from fastapi import FastAPI
from User_route import user_router
from admin_route import admin_router
# from jwt_token import jwt_router
app = FastAPI()

app.include_router(user_router)
app.include_router(admin_router)
