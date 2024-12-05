from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ActionRequest(BaseModel):
    current_action: str = Field(..., description="The current action to analyze")
    user_id: str = Field(..., description="Unique identifier for the user")

class ActionSequence(BaseModel):
    current_action: str
    next_action: str
    confidence: float

class ActionTrackRequest(BaseModel):
    action_name: str = Field(..., description="The action to track")
    user_id: str = Field(..., description="Unique identifier for the user")
    timestamp: Optional[datetime] = Field(default=None, description="Timestamp of the action")
    metadata: Optional[dict] = Field(default=None, description="Additional metadata for the action")

    class Config:
        json_schema_extra = {
            "example": {
                "action_name": "reply",
                "user_id": "user123",
                "timestamp": "2024-01-20T12:00:00",
                "metadata": {"source": "email", "category": "communication"}
            }
        }