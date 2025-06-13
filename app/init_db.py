import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User
from .auth import get_password_hash
import os

logger = logging.getLogger(__name__)

database_url = os.getenv("DATABASE_URL")
if not database_url:
    logger.error("DATABASE_URL is not set")
    raise ValueError("DATABASE_URL not found")

logger.info(f"Connecting to database: {database_url}")
engine = create_engine(database_url)
logger.info("Creating database schema")
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Schema created successfully")
except Exception as e:
    logger.error(f"Failed to create schema: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

users = [
    {"username": "admin", "password": "adminpass", "role": "ADMIN"},
    {"username": "sales", "password": "salespass", "role": "SALES"},
    {"username": "support", "password": "supportpass", "role": "SUPPORT"},
]
for user in users:
    existing_user = db.query(User).filter(User.username == user["username"]).first()
    if not existing_user:
        db.add(User(**user, password=get_password_hash(user["password"])))
        logger.info(f"Added user: {user['username']}")
db.commit()
logger.info("User initialization complete")

db.close()