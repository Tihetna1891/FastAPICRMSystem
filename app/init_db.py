import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User
from .auth import get_password_hash
import os

logger = logging.getLogger(__name__)

database_url = os.getenv("DATABASE_URL")
if not database_url:
    logger.error("DATABASE_URL is not set in the environment")
    raise ValueError("DATABASE_URL environment variable is not set")

logger.info(f"Connecting to database with URL: {database_url}")
engine = create_engine(database_url)
logger.info("Creating database schema")
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

initial_users = [
    {"username": "admin", "password": "adminpass", "role": "ADMIN"},
    {"username": "sales", "password": "salespass", "role": "SALES"},
    {"username": "support", "password": "supportpass", "role": "SUPPORT"},
]

for user_data in initial_users:
    if not db.query(User).filter(User.username == user_data["username"]).first():
        db.add(User(username=user_data["username"], password=get_password_hash(user_data["password"]), role=user_data["role"]))
        logger.info(f"Created user: {user_data['username']}")
db.commit()
logger.info("Database initialization completed")

db.close()