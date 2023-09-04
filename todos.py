from pydantic import BaseModel, EmailStr
from typing import Optional


class user_register(BaseModel):
    name: str
    role: str
    email: EmailStr
    location: str
    phone: int
    password: str


class user_update(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    email: Optional[EmailStr] = None
    location: Optional[str] = None
    phone: Optional[int] = None
    password: Optional[str] = None


class user_login(BaseModel):
    email: EmailStr
    password: str


class jobdata(BaseModel):
    jobid: int
    title: str
    description: str
    salary: int


class ApplyJobData(BaseModel):
    email: EmailStr  # User ID applying for the job
    jobid: int   # Job ID for which the user is applying
