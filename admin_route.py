from schema import list_serial, list_admin_serial, list_job_serial
from database import user_register_collection, admin_collection, job_applies_collection
from fastapi import APIRouter
from bson import ObjectId
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from auth import authenticate_user, create_access_token_for_user, get_current_user
from security import get_password_hash
from pymongo.errors import DuplicateKeyError
from auth import oauth2_scheme, get_current_user
from jose import jwt, JWTError
from auth_config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from todos import jobdata
from pydantic import EmailStr
from auth_bearer import JWTBearer
from auth_handler import signJWT, decodeJWT

admin_router = APIRouter()


@admin_router.post("/admin/login", tags=["Admin"])
async def admin_login(email: EmailStr, password: str):
    if email == "admin@gmail.com" and password == "admin":
        return {"access_token": signJWT(email, role="Admin"), "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


# Get method to view all users
@admin_router.get("/admin/user-profiles", tags=["Admin"])
async def users_info():
    users_info = list_serial(user_register_collection.find())
    return users_info

# Post method to post jobs


@admin_router.post("/admin/post_new_job", dependencies=[Depends(JWTBearer())], tags=["Admin"])
async def post_job(job_data: jobdata):
    # Convert the Pydantic model to a dictionary
    job_dict = job_data.model_dump()

    # Insert the job data into the MongoDB collection
    admin_collection.insert_one(job_dict)

    return {"message": "Job posted successfully"}


# Get method to view job posts
@admin_router.get("/admin/view_job-posts", tags=["Admin"])
async def job_posts():
    job_posts = list_admin_serial(admin_collection.find())
    if not job_posts:
        return {"message": "No jobs available"}
    return job_posts


# Route to get job details with applicantid field
# @admin_router.get("/admin/jobs/{job_id}")
# async def get_job_with_applicantid(job_id: int):
#     job = job_applies_collection.find_one({"jobid": job_id})
#     if job is None:
#         raise HTTPException(status_code=404, detail="Job not found")
#     job_with_applicants = list_job_serial(job)
#     return job_with_applicants

# Get method to view job posts
@admin_router.get("/admin/view-jobs-applies", tags=["Admin"])
async def get_job_with_applicantid():
    job = list_job_serial(job_applies_collection.find())

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job

# Delete request to delete a user


@admin_router.delete("/admin/delete/user/{email}", dependencies=[Depends(JWTBearer())], tags=["Admin"])
async def delete_user(email: EmailStr):
    result = user_register_collection.delete_one({"email": email})

    if result.deleted_count == 0:
        return {"message": "User not found"}

    return {"message": "User deleted successfully", "deleted_email": email}


# Delete request to deleate a job post


@admin_router.delete("/admin/delete_job/{job_id}", dependencies=[Depends(JWTBearer())], tags=["Admin"])
async def delete_job(job_id: int):
    # Check if the job exists
    job = admin_collection.find_one({"jobid": job_id})
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    # Delete the job from the MongoDB collection
    admin_collection.delete_one({"jobid": job_id})

    return {"message": "Job deleted successfully"}
