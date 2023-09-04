# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict
from auth_config import SECRET_KEY, ALGORITHM
import jwt
# from decouple import config


def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string


def signJWT(user_id: str, role: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "user_role": role,
        "expires": time.time() + 1200
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
