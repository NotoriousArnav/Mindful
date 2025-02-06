from argon2 import PasswordHasher, exceptions
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta

# Constants for JWT
SECRET_KEY = "supersecretkey"  # Replace with a secure environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ph = PasswordHasher()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str) -> str:
    """
    Hash a password using Argon2.
    """
    return ph.hash(password)

def verify_password(stored_hash: str, provided_password: str) -> bool:
    """
    Verify a password against its hash.
    """
    try:
        return ph.verify(stored_hash, provided_password)
    except exceptions.VerifyMismatchError:
        return False

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT access token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# get current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
