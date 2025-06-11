from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User
from .auth import get_password_hash
import os
import logging
logger = logging.getLogger(__name__)
logger.info("Initializing database and creating admin user")
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(database_url)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

if not db.query(User).filter(User.username == "admin").first():
    logger.info("Admin user created successfully")
    db.add(User(username="admin", password=get_password_hash("adminpass"), role="ADMIN"))
    db.commit()
else:
    logger.info("Admin user already exists")

db.close()