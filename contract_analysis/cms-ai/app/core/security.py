from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bson import ObjectId
import jwt
from ..core.config import settings
from ..db.mongo import db

bearer_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    # 1) Header present?
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
    token = credentials.credentials

    # 2) Decode JWT
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 3) Extract user id (or email) from payload
    user_id = payload.get("value").get("_id")          # typical claim name
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing subject")

    # 4) Look up user in Mongo
    user_doc = await db.users.find_one(
        {"_id": ObjectId(user_id), "deletedAt": None}
    )
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or deactivated",
        )

    return user_doc 

def role_required(roles: list[str]):
    def _role_checker(user_doc = Depends(get_current_user)):
        if user_doc.get("role") not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user_doc
    return _role_checker
