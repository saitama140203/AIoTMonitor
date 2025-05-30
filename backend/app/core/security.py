from datetime import datetime, timedelta
from typing import Any, List, Optional, Union

from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from app.schemas.user import TokenPayload
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    subject: Union[str, Any], 
    roles: List[str], 
    username: str,
    full_name: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "username": username,
        "full_name": full_name,
        "roles": roles
    }
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def decode_token(token: str) -> Optional[TokenPayload]:
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        payload["roles"] = payload.get("roles", [])
        token_data = TokenPayload(**payload)
        return token_data
    except (jwt.JWTError, ValidationError) as e:
        print(f"Error decoding token: {str(e)}")
        return None