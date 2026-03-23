from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

import jwt
from app.core.config import settings
from app.core.exceptions import *

security = HTTPBearer(auto_error=False)

async def verify_jwt_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:

    # Debug mode -> bypass auth
    if settings.DEBUG:
        return {
            "user_id": "mock-user",
            "email": "nguyentrungan4993@gmail.com",
        }

    if credentials is None:
        raise InvalidTokenException()

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
        )

        user_id = payload.get("sub")
        email = payload.get("email")

        if not user_id:
            raise InvalidTokenException()

        return {
            "user_id": user_id,
            "email": email,
        }

    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()

    except jwt.InvalidTokenError:
        raise InvalidTokenException()