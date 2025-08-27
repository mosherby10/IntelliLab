# backend/app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from a .env file (if present)
load_dotenv()

# Read DATABASE_URL from environment or use a default (postgres)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/intellilab")

# Create SQLAlchemy engine (connects Python to PostgreSQL)
engine = create_engine(DATABASE_URL, echo=False)

# Create a session factory. Each function that talks to DB will use a Session from here.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our ORM models
Base = declarative_base()
