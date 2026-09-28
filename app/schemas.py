"""
schemas.py
Pydantic models used to validate incoming request bodies for the JSON API routes.
"""

from pydantic import BaseModel


class UserInput(BaseModel):
    username: str
    user_id: int
    age: int
    weight: float
    goal: str
    intensity: str  # "low" | "medium" | "high"


class FeedbackRequest(BaseModel):
    feedback: str


class WorkoutRequest(BaseModel):
    goal: str
    intensity: str
