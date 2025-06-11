from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from .models import Base  # Add this import

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
# Base.metadata.create_all(bind=engine)  # Enable this

def get_db():
    db = Session(bind=engine.connect())
    try:
        yield db
    finally:
        db.close()