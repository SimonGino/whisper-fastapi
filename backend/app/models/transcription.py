# app/models/transcription.py

from typing import Optional
from pydantic import BaseModel, Field


class TranscriptionSegment(BaseModel):
    start: float = Field(default=0)
    end: Optional[float] = None
    text: str = Field(default="")
