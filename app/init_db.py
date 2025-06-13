import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User
from .auth import get_password_hash

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL is not set")
        raise ValueError("DATABASE_URL not found")

    logger.info(f"Connecting to database: {database_url}")
    engine = create_engine(database_url)
    logger.info("Attempting to create database schema")
    Base.metadata.create_all(bind=engine)
    logger.info("Schema created successfully")
except Exception as e:
    logger.error(f"Schema creation failed: {str(e)}")
    raise

try:
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
except Exception as e:
    logger.error(f"User initialization failed: {str(e)}")
    db.rollback()
    raise
finally:
    db.close()