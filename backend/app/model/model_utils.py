from transformers import AutoTokenizer, pipeline
from app.model.mhp_classifier import MHP_Classifier
import torch
import os
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

def remove_stopwords(text):
    new_list = []
    words = word_tokenize(text)
    stopwrds = stopwords.words('english')
    for word in words:
        if word not in stopwrds:
            new_list.append(word)
    return ' '.join(new_list)

def load_model(config: dict):
    """
    Load the fine-tuned model from a checkpoint
    """
    checkpoint_path = os.path.join(os.path.dirname(__file__), "fine_tuned_model.ckpt")
    model = MHP_Classifier.load_from_checkpoint(checkpoint_path, config=config)
    model.eval()
    return model

def predict_emotion(model, text: str, tokenizer, emotion_pipeline):
    """
    Predict emotions and unhealthy comment status for a given text.
    """
    print("Entering predict emotion")
    # Extract emotion scores
    text = text.lower()
    exclude = string.punctuation
    text = text.translate(str.maketrans('', '', exclude))
    text = remove_stopwords(text)
    print("removed stopwords")
    print(text)
    emotion_scores = emotion_pipeline(text)
    print(emotion_scores)

    # Convert emotion scores to a tensor
    # Drop the last feature by slicing off the last element
    print("Getting emotion features")
    emotion_features = torch.tensor([score['score'] for score in emotion_scores[0]])
    print(emotion_features)


    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # Model prediction
    with torch.no_grad():
        logits = model(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            emotion_features=emotion_features.unsqueeze(0)
        )[1]  # Get logits

    predicted_class = torch.sigmoid(logits)
    print(predicted_class)
    predicted_class = torch.round(predicted_class).item()
    print(predicted_class)

    # Prepare the response with emotions and prediction result
    return {
        "emotions": [{score['label']: score['score']} for score in emotion_scores[0]],
        "prediction": "Unhealthy" if predicted_class == 1 else "Healthy"
    }
