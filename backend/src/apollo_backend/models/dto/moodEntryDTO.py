from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MoodEntryCreateDTO(BaseModel):
    """DTO per crear una nova entrada."""
    text: str = Field(..., min_length=1, max_length=2000)
    mood: int = Field(..., ge=1, le=5)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD
    time: str = Field(..., pattern=r"^\d{2}:\d{2}$")  # HH:MM


class MoodEntryUpdateDTO(BaseModel):
    """DTO per actualitzar una entrada."""
    text: Optional[str] = Field(None, min_length=1, max_length=2000)
    mood: Optional[int] = Field(None, ge=1, le=5)


class MoodEntryResponseDTO(BaseModel):
    """DTO per retornar una entrada."""
    id: int
    text: str
    mood: int
    date: str
    time: str
    created_at: datetime

    class Config:
        from_attributes = True


class MoodEntryListResponseDTO(BaseModel):
    """DTO per retornar múltiples entrades agrupades per dia."""
    date: str
    entries: list[MoodEntryResponseDTO]
