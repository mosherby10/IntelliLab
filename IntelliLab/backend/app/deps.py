# backend/app/deps.py
from .database import SessionLocal
from fastapi import Depends

def get_db():
    """
    Dependency that yields a database session and closes it after use.
    Use in endpoints with: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
