from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.user import UserResponse
from app.services.user import get_users
from ...v1.deps import get_db, get_current_active_admin_or_teamlead
from app.models.user import User
router = APIRouter()


@router.get("", response_model=List[UserResponse])
def fetch_users_with_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_or_teamlead)
):
    return get_users(db=db, skip=skip, limit=limit, current_user=current_user)