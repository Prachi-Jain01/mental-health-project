from fastapi import FastAPI, HTTPException
from app.config import config
from app.model.model_utils import load_model, predict_emotion
from app.schemas import CommentRequest, CommentResponse
from transformers import AutoTokenizer, pipeline
import torch

from fastapi.middleware.cors import CORSMiddleware


# Your existing code...
app = FastAPI()

# Allow requests from React (running on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app = FastAPI()

# Load tokenizer and emotion pipeline at startup
tokenizer = AutoTokenizer.from_pretrained(config["model_name"])
print("Loading emotion_pipeline")
emotion_pipeline = pipeline(
    "text-classification",
    model="nateraw/bert-base-uncased-emotion",
    return_all_scores=True,
    truncation=True,
    max_length=512
)
print("Emotion pipeline loaded")

# Load the MHP classifier model from checkpoint
print("Loading model")
model = load_model(config=config)
print("Model loaded")
@app.post("/predict", response_model=CommentResponse)
async def predict_comment(request: CommentRequest):
    print("Starting emotion prediction")
    try:
        # Predict emotion and unhealthy status
        result = predict_emotion(model, request.text, tokenizer, emotion_pipeline)
        print("callign predict")
        # Return response in the defined format
        return CommentResponse(
            text=request.text,
            emotions=result["emotions"],
            prediction=result["prediction"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    print("Emotion detected")