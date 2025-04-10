from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any, Dict

from ...v1.deps import get_db, get_current_user, get_current_active_admin
from app.schemas.user import (
    User, UserCreate, Token, UserPasswordUpdate, 
    UserPasswordReset, UserCreateOperator, UserCreateSupervisor, UserCreateTeamLead
)
from app.services.user import (
    login, create_user, update_password, reset_password,
    create_operator, create_supervisor, create_team_lead
)
from app.models.user import UserRole


router = APIRouter()


@router.post("/login", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Admin login - lấy token truy cập
    """
    return login(db, form_data.username, form_data.password)


@router.put("/reset-password", status_code=status.HTTP_200_OK)
def reset_user_password(
    reset_data: UserPasswordReset,
    current_user: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Admin đặt lại mật khẩu người dùng
    """
    new_password = reset_password(db, email=reset_data.email)
    return {
        "message": "Đặt lại mật khẩu thành công",
        "temp_password": new_password,
        "email": reset_data.email
    }


@router.put("/update-password", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def update_user_password(
    password_update: UserPasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Admin (hoặc bất kỳ người dùng nào) cập nhật mật khẩu của mình
    """
    user = update_password(db, current_user.id, password_update)
    return {"message": "Cập nhật mật khẩu thành công"}


@router.post("/create-operator", response_model=User, status_code=status.HTTP_201_CREATED)
def create_operator_user(
    user_in: UserCreateOperator,
    current_user: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    Admin tạo người dùng mới với vai trò Operator
    """
    return create_operator(db, user_in)


@router.post("/create-supervisor", response_model=User, status_code=status.HTTP_201_CREATED)
def create_supervisor_user(
    user_in: UserCreateSupervisor ,
    current_user: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    Admin tạo người dùng mới với vai trò Supervisor
    """
    return create_supervisor(db, user_in)


@router.post("/create-team-lead", response_model=User, status_code=status.HTTP_201_CREATED)
def create_team_lead_user(
    user_in: UserCreateTeamLead,
    current_user: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    Admin tạo người dùng mới với vai trò Team Lead
    """
    return create_team_lead(db, user_in)