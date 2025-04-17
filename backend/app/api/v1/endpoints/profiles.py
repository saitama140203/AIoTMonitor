from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.profile import ProfileCreate, ProfileResponse
from app.services.profile_sevice import create_profile
from app.api.v1.deps import get_db, get_current_team_lead
from app.models.user import User

router = APIRouter()

@router.post("/create_profile", 
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_profile(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_team_lead)
):
    return create_profile(db, profile_data, current_user)