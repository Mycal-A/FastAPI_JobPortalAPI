from todos import user_register, user_update, ApplyJobData
from schema import list_serial, list_admin_serial, list_job_serial, individual_adminserial, list_user_serial
from database import user_register_collection, admin_collection, job_applies_collection
from fastapi import APIRouter
from bson import ObjectId
from fastapi import FastAPI, Depends, HTTPException, status
from datetime import timedelta
from pymongo.errors import DuplicateKeyError
from jose import jwt, JWTError
from auth_config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from auth_handler import signJWT, decodeJWT
from pydantic import EmailStr
from auth_bearer import JWTBearer


user_router = APIRouter()


# Post method for User registration
@user_router.post("/user_register", tags=["User"])
async def user_register(user_data: user_register):
    # Convert Pydantic model to dictionary
    user_dict = user_data.dict()
    # Hash the password
    # hashed_password = get_password_hash(user_dict["password"])

    try:
        # Attempt to insert the user data
        result = user_register_collection.insert_one(user_dict)
        response = {"message": "User registered successfully",
                    "inserted_id": str(result.inserted_id)}
        return signJWT(user_data.email, role="User")
    except DuplicateKeyError:
        response = {"message": "Email already registered"}

    return response

# Post method to login with auth
# @user_router.post("/login", tags=["User"])
# async def login_for_access_token(email: EmailStr, password: str):
#     # Query the user data based on the provided email
#     user_data = user_register_collection.find_one({"email": email})
#     if user_data:
#         hashed_password = user_data.get("password")
#         if hashed_password and verify_password(password, hashed_password):
#             return {"access_token": signJWT(user_data.email), "token_type": "bearer"}

#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Incorrect email or password",
#         headers={"WWW-Authenticate": "Bearer"},
#     )


@user_router.post("/user/login", tags=["User"])
async def login_for_access_token(email: EmailStr, password: str):
    # Query the user data based on the provided email
    user_data = user_register_collection.find_one({"email": email})

    if user_data and user_data["password"] == password:
        return {"access_token": signJWT(user_data["email"], role="User"), "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


# get method to retrive a specific user
@user_router.get("/user/{email}", tags=["User"])
async def get_user_by_email(email: str):
    userdata = user_register_collection.find_one({"email": email})
    if userdata is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Wrap the userdata in a list and pass it to list_serial
    serialized_user = list_serial([userdata])
    return serialized_user

# Put method to update user details


@user_router.put("/user/profile/{email}", dependencies=[Depends(JWTBearer())], tags=["User"])
async def update_user(email: EmailStr, updated_fields: user_update):
    existing_user = user_register_collection.find_one(
        {"email": email})
    if existing_user is None:
        return {"message": "User not found"}

    # Update only the desired fields
    update_data = {}
    for field, value in updated_fields.dict().items():
        if value is not None:
            update_data[field] = value

    if update_data:
        user_register_collection.update_one(
            {"email": email}, {"$set": update_data})

    return {"message": "User updated successfully"}


# # Get method to view job posts
@user_router.get("/view_job_posts", tags=["User"])
async def job_posts():
    job_posts = list_admin_serial(admin_collection.find())
    if not job_posts:
        return {"message": "No jobs available"}
    return job_posts


# User route to apply for a job
@user_router.post("/user/apply_job", dependencies=[Depends(JWTBearer())], tags=["User"])
async def apply_for_job(apply_job_data: ApplyJobData):
    email = apply_job_data.email
    job_id = apply_job_data.jobid

    job = admin_collection.find_one({"jobid": job_id})
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    # Update the applicants field in MongoDB
    job_applies_collection.update_one(
        {"jobid": job_id}, {"$addToSet": {"email": email}}, upsert=True)

    return {"message": "Application submitted successfully"}
