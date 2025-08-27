# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    is_instructor: Optional[bool] = False

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_instructor: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class SubmissionCreate(BaseModel):
    course: str
    content: str

class SubmissionOut(SubmissionCreate):
    id: int
    user_id: int
    score: Optional[float]
    created_at: datetime.datetime

    class Config:
        orm_mode = True
