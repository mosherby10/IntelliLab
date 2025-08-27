# backend/app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..deps import get_db
from .auth import oauth2_scheme, get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schemas.UserOut)
def read_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Simple endpoint to get current user's profile using a bearer token.
    """
    payload = get_current_user(token, db)
    return payload
