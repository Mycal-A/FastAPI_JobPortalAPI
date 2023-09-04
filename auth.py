from datetime import timedelta
import jwt
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from security import verify_password, create_access_token
from database import user_register_collection
from auth_config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(email: str, password: str):
    user = user_register_collection.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return False
    return user

def create_access_token_for_user(user):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return access_token

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_register_collection.find_one({"email": email})
    if user is None:
        raise credentials_exception
    return user
