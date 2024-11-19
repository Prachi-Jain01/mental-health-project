import os
config = {
    "model_name": "distilroberta-base",  # Hugging Face model name
    "checkpoint_path": os.path.join(os.path.dirname(__file__), "model/fine_tuned_model.ckpt"),  # Path to the model checkpoint
    "emotion_attributes": ["sadness", "joy", "love", "anger", "fear", "surprise"],
    "n_labels": 1,  # Binary classification
}