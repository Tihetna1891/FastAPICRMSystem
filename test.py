from app.crud import create_user
from app.models import UserRole
from app.database import get_db

db = next(get_db())
create_user(db, "admin", "adminpass", UserRole.ADMIN)  # Use enum member directly
create_user(db, "sales", "salespass", UserRole.SALES)
create_user(db, "support", "supportpass", UserRole.SUPPORT)
db.close()
print("Users created and database initialized successfully!")
# import secrets
# print(secrets.token_hex(32))  # Generates a 64-character hex string

# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# print(pwd_context.hash("testpass"))