from pydantic import BaseModel, Field
from typing import Optional, List


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=50000)
    max_length: Optional[int] = Field(default=500, ge=100, le=2000)
    focus_areas: Optional[List[str]] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "This engineering specification document outlines the requirements for the industrial control system upgrade at Plant B. All PLC controllers must comply with IEC 61511 standards.",
                "max_length": 300,
                "focus_areas": ["requirements", "risks"],
            }
        }
    }


class AskRequest(BaseModel):
    question: str = Field(..., min_length=10, max_length=1000)
    context: str = Field(..., min_length=50, max_length=50000)

    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "What are the main safety requirements for the PLC upgrade?",
                "context": "This document describes the safety and compliance requirements for the PLC upgrade project. All controllers must meet IEC 61511 safety standards and include redundant power supply units.",
            }
        }
    }


class SummarizeResponse(BaseModel):
    summary: str
    word_count: int
    key_points: List[str]
    model_used: str
    processing_time_ms: float


class AskResponse(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    sources: List[str]
    model_used: str
    processing_time_ms: float


class HealthResponse(BaseModel):
    status: str
    version: str
    ai_backend: str
    uptime_seconds: float