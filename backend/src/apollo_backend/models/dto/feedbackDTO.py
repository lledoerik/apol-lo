from pydantic import BaseModel, Field
from typing import Dict, Optional


class FeedbackRequestDTO(BaseModel):
    """Request per guardar feedback de l'usuari"""
    text: str = Field(..., min_length=1, max_length=1000)

    # Predicció original
    predicted_label: str = Field(...)  # negative/neutral/positive
    predicted_probabilities: Dict[str, float] = Field(...)
    predicted_mood: int = Field(..., ge=1, le=5)

    # Correcció de l'usuari
    corrected_mood: int = Field(..., ge=1, le=5)

    model_config = {"extra": "forbid"}


class FeedbackResponseDTO(BaseModel):
    """Response després de guardar feedback"""
    id: int
    was_corrected: bool
    message: str

    model_config = {"from_attributes": True, "extra": "forbid"}
