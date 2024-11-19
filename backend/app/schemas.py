from pydantic import BaseModel
from typing import List, Dict

class CommentRequest(BaseModel):
    text: str

class CommentResponse(BaseModel):
    text: str
    emotions: List[Dict[str, float]]
    prediction: str