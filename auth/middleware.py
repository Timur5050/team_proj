import jwt
from fastapi.requests import Request
from fastapi import HTTPException

from auth.utils import decode_jwt


def get_user_id(request: Request):
    token = None

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")

    if not token:
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=400, detail="Authorization token not found")

    try:
        content = decode_jwt(token)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Expired token")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid token")

    return content["user_id"]
