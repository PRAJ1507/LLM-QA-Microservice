from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


# Enum matching the one in models.py
class QuestionStatus(str, Enum):
    pending = "pending"
    answered = "answered"


# ---------------------------
# Document Schemas
# ---------------------------

class DocumentCreate(BaseModel):
    title: str
    content: str


class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True


# ---------------------------
# Question Schemas
# ---------------------------

class QuestionCreate(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    id: int
    document_id: int
    question: str
    answer: Optional[str] = None
    status: QuestionStatus
    created_at: datetime

    class Config:
        orm_mode = True
