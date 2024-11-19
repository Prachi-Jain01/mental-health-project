from transformers import AutoModel, AdamW, get_cosine_schedule_with_warmup
import torch.nn as nn
import torch
import math
import torch.nn.functional as F
import pytorch_lightning as pl

class MHP_Classifier(pl.LightningModule):
    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.pretrained_model = AutoModel.from_pretrained(config['model_name'], return_dict=True)
        self.hidden = torch.nn.Linear(self.pretrained_model.config.hidden_size + len(config['emotion_attributes']), 
                                      self.pretrained_model.config.hidden_size)  # Adding emotion feature size
        self.classifier = torch.nn.Linear(self.pretrained_model.config.hidden_size, self.config['n_labels'])  # Final output
        torch.nn.init.xavier_uniform_(self.classifier.weight)
        self.loss_func = nn.BCEWithLogitsLoss(reduction='mean')
        self.dropout = nn.Dropout()

    def forward(self, input_ids, attention_mask, emotion_features, labels=None):
        # Extract features from the RoBERTa model
        output = self.pretrained_model(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = torch.mean(output.last_hidden_state, 1)

        # Concatenate text features with emotion features
        combined_output = torch.cat((pooled_output, emotion_features), dim=1)

        # Pass through hidden layer
        combined_output = self.dropout(combined_output)
        combined_output = self.hidden(combined_output)
        combined_output = F.relu(combined_output)
        combined_output = self.dropout(combined_output)

        # Classifier layer
        logits = self.classifier(combined_output)

        # Calculate loss
        loss = 0
        if labels is not None:
            loss = self.loss_func(logits.view(-1, self.config['n_labels']), labels.view(-1, self.config['n_labels']))

        return loss, logits

    def training_step(self, batch, batch_index):
        loss, outputs = self(**batch)
        self.log("train_loss", loss, prog_bar=True, logger=True)
        return {"loss": loss, "predictions": outputs, "labels": batch["labels"]}

    def validation_step(self, batch, batch_index):
        loss, outputs = self(**batch)
        self.log("val_loss", loss, prog_bar=True, logger=True)
        return {"val_loss": loss, "predictions": outputs, "labels": batch["labels"]}

    def predict_step(self, batch, batch_index):
        loss, outputs = self(**batch)
        return outputs

    def configure_optimizers(self):
        optimizer = AdamW(self.parameters(), lr=self.config['lr'], weight_decay=self.config['weight_decay'])
        total_steps = self.config['train_size'] / self.config['batch_size']
        warmup_steps = math.floor(total_steps * self.config['warmup'])
        scheduler = get_cosine_schedule_with_warmup(optimizer, warmup_steps, total_steps)
        return [optimizer], [scheduler]


# Example configuration (replace with actual values)
emotion_attributes = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']
config = {
    'model_name': 'distilroberta-base',  # Model name (DistilRoBERTa)
    'n_labels': 1,  # Binary classification (healthy vs unhealthy)
    'batch_size': 128,  # Batch size
    'lr': 1.5e-6,  # Learning rate
    'warmup': 0.2,  # Warmup proportion
    'train_size': 10000,  # Example size, replace with actual
    'weight_decay': 0.001,  # Weight decay for optimizer
    'n_epochs': 20,  # Number of epochs
    'emotion_attributes': emotion_attributes,  # List of emotion-related columns in the dataset
}