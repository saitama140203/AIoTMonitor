from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any, Dict
from typing import List
from app.api.v1.deps import get_db, get_current_user, get_current_admin
from app.schemas.user import (
    UserCreate, Token, UserPasswordUpdate,
    UserPasswordReset, UserResponse
)
from app.services.user import (
    login, update_password, reset_password, create_user_with_roles, get_roles
)
from app.models.user import User

router = APIRouter()

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Đăng nhập và nhận token truy cập (cho mọi role)
    """
    try:
        result = login(db, form_data.username, form_data.password)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi đăng nhập: {str(e)}"
        )

@router.put("/reset-password", status_code=status.HTTP_200_OK)
def reset_user_password(
    reset_data: UserPasswordReset,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> Dict[str, Any]:
    """
    Admin reset mật khẩu người dùng khác
    """
    try:
        new_password = reset_password(db, email=reset_data.email)
        return {
            "message": "Đặt lại mật khẩu thành công",
            "temp_password": new_password,
            "email": reset_data.email
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi reset mật khẩu: {str(e)}"
        )

@router.put("/update-password", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def update_user_password(
    password_update: UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Cập nhật mật khẩu cho user hiện tại
    """
    try:
        user = update_password(db, current_user.id, password_update)
        return {"message": "Cập nhật mật khẩu thành công"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi cập nhật mật khẩu: {str(e)}"
        )

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    try:
        return create_user_with_roles(db, user_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi hệ thống khi tạo user: {str(e)}"
        )
    
    
@router.get("/roles", status_code=status.HTTP_200_OK)
def admin_get_roles(  
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)) -> List[str]:
    roles = get_roles(db)
    return roles
