from typing import Optional, List, Any, Dict
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
import secrets
import string
from random import choice

from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, Token, UserPasswordUpdate


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def login(db: Session, username: str, password: str) -> Dict[str, Any]:
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai tên đăng nhập hoặc mật khẩu",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản đã bị vô hiệu hóa",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, role=user.role, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
    }


def create_user(db: Session, user_in: UserCreate) -> User:

    if get_user_by_username(db, username=user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên đăng nhập đã tồn tại trong hệ thống",
        )
    if get_user_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã tồn tại trong hệ thống",
        )
    
    # Create new user
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_password,
        role=user_in.role,
        is_active=True,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_operator(db: Session, user_in: UserCreate) -> User:
    user_data = user_in.dict()
    print("Creating operator user with data:", user_data)
    user_data["role"] = UserRole.OPERATOR
    user_create = UserCreate(**user_data)
    return create_user(db=db, user_in=user_create)


def create_supervisor(db: Session, user_in: UserCreate) -> User:
    user_data = user_in.dict()
    user_data["role"] = UserRole.SUPERVISOR
    user_create = UserCreate(**user_data)
    return create_user(db=db, user_in=user_create)


def create_team_lead(db: Session, user_in: UserCreate) -> User:
    user_data = user_in.dict()
    user_data["role"] = UserRole.TEAM_LEAD
    user_create = UserCreate(**user_data)
    return create_user(db=db, user_in=user_create)


def update_password(db: Session, user_id: int, password_update: UserPasswordUpdate) -> User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy người dùng",
        )
    
    # Verify current password
    if not verify_password(password_update.current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu hiện tại không chính xác",
        )
    
    # Update password
    hashed_password = get_password_hash(password_update.new_password)
    user.hashed_password = hashed_password
    
    db.commit()
    db.refresh(user)
    return user


def generate_random_password(length: int = 12) -> str:
    """Generate a secure random password with specified length"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(choice(alphabet) for _ in range(length))


def reset_password(db: Session, email: str) -> str:
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy người dùng với email này",
        )
    
    # Generate new random passwor
    new_password = generate_random_password()
    

    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    
    db.commit()

    return new_password