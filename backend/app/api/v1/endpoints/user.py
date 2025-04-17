from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.user import User as UserSchema
from app.services.user import get_users
from ...v1.deps import get_db, get_current_active_admin_or_teamlead

router = APIRouter()



@router.get("/", response_model=List[UserSchema])
def fetch_users(
    role: Optional[str] = None,
    skip: int = 0,
    limit: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin_or_teamlead)
):
    return get_users(db, role=role, skip=skip, limit=limit)

