from typing import Generator, Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm.exc import NoResultFound

from app.db.session import SessionLocal
from app.core.config import settings
from app.core.security import decode_token
from app.models.user import User, UserRole, Role
from app.schemas.user import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> User:
    try:
        # Giải mã token và xác thực
        token_data = decode_token(token)
        if not token_data or not token_data.sub:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        
        # Lấy user kèm roles từ database
        user = db.query(User).options(
            joinedload(User.roles).joinedload(UserRole.role)
        ).filter(User.id == token_data.sub).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
        
        return user

    except (jwt.JWTError, ValidationError, NoResultFound) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

def role_required(required_roles: List[str]):
    def role_checker(user: User = Depends(get_current_user)):
        # Lấy danh sách role names
        user_roles = [role.role.name for role in user.roles]
        
        # Kiểm tra có ít nhất 1 role trùng khớp
        if not any(role in required_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return role_checker

def get_current_admin(user: User = Depends(role_required(["admin"]))):
    return user

def get_current_team_lead(user: User = Depends(role_required(["team_lead"]))):
    return user

def get_current_supervisor(user: User = Depends(role_required(["supervisor"]))):
    return user

def get_current_operator(user: User = Depends(role_required(["operator"]))):
    return user

def allow_roles(roles: List[str]):
    return Depends(role_required(roles))

def get_all_operators(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
) -> List[User]:
    try:
        if not any(role.role.name in ["admin", "team_lead"] for role in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Require Admin or Team Lead"
            )
        
        operators = db.query(User).filter(User.is_active == True).all()
        return operators

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching operators: {str(e)}"
        )
    return current_user

def get_current_active_admin_or_teamlead(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEAM_LEAD:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập chức năng này",
        )
    return current_user
