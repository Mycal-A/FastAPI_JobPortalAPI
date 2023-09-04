from todos import user_register,user_update,ApplyJobData
from schema import list_serial,list_admin_serial,list_job_serial
from database import user_register_collection,admin_collection,job_applies_collection
from fastapi import APIRouter
from bson import ObjectId
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from auth import authenticate_user, create_access_token_for_user, get_current_user
from security import get_password_hash
from pymongo.errors import DuplicateKeyError
from auth import oauth2_scheme,get_current_user
from jose import jwt,JWTError
from auth_config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

jwt_router = APIRouter()

#Post method to login with auth
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token_for_user

jwt_router = APIRouter()

@jwt_router.post("/auth/login", tags=["User JWT"], response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password
    
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token_for_user(user)
    return {"access_token": access_token, "token_type": "bearer"}

# Add JWT security requirement for the router
jwt_security = OAuth2PasswordBearer(tokenUrl="/jwt/auth/login")  # Adjust the URL if needed
jwt_router.include_router(jwt_router, dependencies=[Depends(jwt_security)])



@jwt_router.put("/user/update_profile", tags=["User JWT"])
async def update_user_profile(
    updated_fields: user_update,
    current_user: dict = Depends(get_current_user)
):
    email = current_user["email"]
    existing_user = user_register_collection.find_one({"email": email})
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    update_data = {}
    for field, value in updated_fields.dict().items():
        if value is not None:
            update_data[field] = value
    
    if update_data:
        user_register_collection.update_one({"email": email}, {"$set": update_data})
    
    return {"message": "User profile updated successfully"}