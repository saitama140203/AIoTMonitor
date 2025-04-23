from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
import secrets
import string
from random import choice

from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from app.models.user import User, UserRole, Role
from app.schemas.user import UserCreate, UserPasswordUpdate, UserResponse


from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user import User, UserRole


def get_users(
        db: Session,
        role: Optional[str] = None,
        skip: int = 0,
        limit: Optional[int] = None
) -> List[User]:
    query = db.query(User)

    if role:
        try:
            role_enum = UserRole[role.upper()]
            query = query.filter(User.role == role_enum)
        except KeyError:
            return []

    if skip:
        query = query.offset(skip)

    if limit:
        query = query.limit(limit)

    return query.all()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
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
    
    # Lấy danh sách roles
    user_roles = [role.role.name for role in user.roles]
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id,
        roles=user_roles,
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "roles": user_roles,
    }

def create_user_with_roles(db: Session, user_in: UserCreate) -> User:
    if get_user_by_username(db, user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên đăng nhập đã tồn tại trong hệ thống",
        )
        
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã tồn tại trong hệ thống",
        )
    
    roles = []
    for role_name in user_in.roles:
        role = (db.query(Role).filter(Role.name == role_name.lower(), Role.name != "admin").first())
        if not role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role không hợp lê, vui lòng kiểm tra lại !!!"
            )
        else:
            roles.append(role)   

    hashed_password = get_password_hash(user_in.password)
    
    db_user = User(
        username=user_create.username,
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=hashed_password,
        is_active=True
    )
    try:  
              
        db.add(db_user)
        db.flush()

        for role in roles:
            user_role = UserRole(user_id=db_user.id, role_id=role.id)
            db.add(user_role)

        db.commit()
        db.refresh(db_user)

        # return db_user
        role_names = [role.role.name for role in db_user.roles]
    
        return UserResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            full_name=db_user.full_name,
            is_active=db_user.is_active,
            roles=role_names,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi tạo người dùng: {str(e)}"
        )
        role=user_create.role,
        is_active=True,
    )
   

def update_password(db: Session, user_id: int, password_update: UserPasswordUpdate) -> User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy người dùng",
        )
    
    if not verify_password(password_update.current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu hiện tại không chính xác",
        )
    
    hashed_password = get_password_hash(password_update.new_password)
    user.hashed_password = hashed_password
    
    try:
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi cập nhật mật khẩu: {str(e)}"
        )

def get_roles(db: Session) -> List[str]:
    roles = db.query(Role).filter(Role.name != "admin").all()
    return [role.name for role in roles]


def generate_random_password(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))

def reset_password(db: Session, user_name: str) -> str:
    user = get_user_by_username(db, user_name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy người dùng với user này",
        )
    
    new_password = "abc123@@"
    user.hashed_password = get_password_hash(new_password)
    
    try:
        db.flush()
        db.commit()
        return new_password
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi đặt lại mật khẩu: {str(e)}"
        )