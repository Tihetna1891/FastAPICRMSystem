# from fastapi import FastAPI, Depends, Request, Form, HTTPException
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.templating import Jinja2Templates
# from .auth import create_access_token, get_current_user, verify_password
# from .crud import create_user, create_customer, get_customers
# from .database import get_db
# from sqlalchemy.orm import Session
# from starlette.status import HTTP_302_FOUND
# from .models import User
# import logging

# app = FastAPI()
# templates = Jinja2Templates(directory="app/templates")
# logger = logging.getLogger(__name__)

# @app.get("/", response_class=HTMLResponse)
# async def login_form(request: Request):
#     logger.info("Login form accessed")
#     return templates.TemplateResponse("base.html", {"request": request, "content": "<h1>CRM Login</h1><form method='post' action='/token'><input type='text' name='username' placeholder='Username'><input type='password' name='password' placeholder='Password'><input type='submit' value='Login'></form>"})

# @app.post("/token")
# async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == username).first()
#     if not user or not verify_password(password, user.password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     access_token = create_access_token(data={"sub": username})
#     response = RedirectResponse(url=f"/{user.role.value}", status_code=HTTP_302_FOUND)
#     response.set_cookie(key="token", value=access_token, httponly=True, max_age=1800)
#     return response

# @app.get("/{role}", response_class=HTMLResponse)

# async def dashboard(request: Request, role: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     logger.info(f"Checking role: user.role.value={user.role.value}, role={role}")
#     if user.role.value != "ADMIN" and user.role.value.lower() != role.lower():
#         raise HTTPException(status_code=403, detail="Access denied")
#     customers = get_customers(db, role)
#     return templates.TemplateResponse(f"{role}.html", {"request": request, "customers": customers})

# @app.post("/customers")
# async def create_customer_endpoint(name: str = Form(...), email: str = Form(...), status: str = Form(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     if user.role.value != "ADMIN":
#         raise HTTPException(status_code=403, detail="Access denied")
#     create_customer(db, name, email, status)
#     return RedirectResponse(url="/admin", status_code=HTTP_302_FOUND)

# @app.get("/logout")
# async def logout(request: Request):
#     logger.info("Logout initiated")
#     response = RedirectResponse(url="/", status_code=HTTP_302_FOUND)
#     response.delete_cookie("token")
#     return response

from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .auth import create_access_token, get_current_user, verify_password
from .crud import create_user, create_customer, get_customers
from .database import get_db
# from . import models, crud, auth, database
from sqlalchemy.orm import Session
from starlette.status import HTTP_302_FOUND
from .models import User
import logging

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)

@app.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    logger.info("Login form accessed")
    return templates.TemplateResponse("base.html", {"request": request, "content": "<h1>CRM Login</h1><form method='post' action='/token'><input type='text' name='username' placeholder='Username'><input type='password' name='password' placeholder='Password'><input type='submit' value='Login'></form>"})

@app.post("/token")
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    logger.info(f"Login attempt for username: {username}")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        logger.error(f"User {username} not found")
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(password, user.password):
        logger.error(f"Password mismatch for user {username}")
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": username})
    logger.info(f"Generated access token for {username}: {access_token[:10]}...")  # Log first 10 chars for security
    response = RedirectResponse(url=f"/{user.role.value.lower()}", status_code=HTTP_302_FOUND)  # Convert to lowercase
    response.set_cookie(key="token", value=access_token, httponly=True, max_age=1800)
    logger.info(f"Cookie set, redirecting to /{user.role.value.lower()}")
    return response

@app.get("/admin", response_class=HTMLResponse)
@app.get("/sales", response_class=HTMLResponse)
@app.get("/support", response_class=HTMLResponse)
async def dashboard(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    role = request.url.path.split("/")[-1]
    logger.info(f"Dashboard accessed: user.role.value={user.role.value}, role={role}")
    if user.role.value != "ADMIN" and user.role.value.lower() != role:
        raise HTTPException(status_code=403, detail="Access denied")
    customers = get_customers(db, role)
    return templates.TemplateResponse(f"{role}.html", {"request": request, "customers": customers})

@app.post("/customers")
async def create_customer_endpoint(name: str = Form(...), email: str = Form(...), status: str = Form(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role.value != "ADMIN":
        raise HTTPException(status_code=403, detail="Access denied")
    create_customer(db, name, email, status)
    return RedirectResponse(url="/admin", status_code=HTTP_302_FOUND)

@app.get("/logout")
async def logout(request: Request):
    logger.info("Logout endpoint hit")
    try:
        response = RedirectResponse(url="/", status_code=HTTP_302_FOUND)
        response.delete_cookie("token")
        logger.info("Cookie deleted, redirecting to /")
        return response
    except Exception as e:
        logger.error(f"Logout failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Logout error: {str(e)}")