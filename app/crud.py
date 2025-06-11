from sqlalchemy.orm import Session
from .models import UserRole, User, Customer
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from .auth import get_password_hash
from .database import get_db  # Import get_db from database.py
load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://crm_user:securepassword@localhost/crm_db")
# engine = create_engine(DATABASE_URL)
# Base.metadata.create_all(bind=engine)


def create_user(db: Session, username: str, password: str, role: str):
    hashed_password = get_password_hash(password)  # From auth.py
    db_user = User(username=username, password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_customer(db: Session, name: str, email: str, status: str):
    db_customer = Customer(name=name, email=email, status=status)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customers(db: Session, role: str):
    if role.lower() == "admin":
        return db.query(Customer).all()
    elif role.lower() == "sales":
        return db.query(Customer).filter(Customer.status.in_(["New", "In Progress"])).all()
    elif role.lower() == "support":
        return db.query(Customer).filter(Customer.status == "Resolved").all()
    return []