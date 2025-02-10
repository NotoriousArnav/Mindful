from security import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas import User, FullUser, AbsUser, UserCreate, UserLogin
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pprint import pprint
from routes import router
from database import db

app = FastAPI(
    title="Mindful",
    description="API for Mindful",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.post("/signup")
async def signup(user: UserCreate):

    hashed_password = hash_password(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "profile_image": user.profile_image,
    }
    # Check for conflicts
    existing_user = await db.get_user(email=user.email) or await db.get_user(username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user_id = await db.insert_user(user_data)
    access_token = create_access_token({"sub": user_data.get("email")})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.get_user(email=form_data.username) or await db.get_user(username=form_data.username)
    exception = HTTPException(status_code=401, detail="Invalid username or password")
    if not verify_password(user["password"], form_data.password) or not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token({"sub": user.get("email")})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/ping")
async def root():
    """Ping Endpoint for testing"""
    return {"message": "Hello World"}
