# backend/app/main.py
from fastapi import FastAPI
from .database import engine
from . import models
from .routers import auth, users, ml_router, nlp_router

# Create all DB tables (simple approach for a starter project)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="IntelliLab API")

# include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ml_router.router)
app.include_router(nlp_router.router)
