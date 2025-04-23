from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.profile import ProfileCreate, ProfileResponse, AssignProfile, AssignProfileResponse
from app.services.profile_sevice import create_profile, assign_profile, get_all_profiles, add_list_command_to_profile
from app.api.v1.deps import get_db, get_current_team_lead, get_current_user
from app.models.user import User
from app.schemas.profile import ProfileCommandRequest,ProfileCommandResponse

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

@router.post("/assign_profile",)
def assign_profile_operator(
    assign_profile_data: AssignProfile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_team_lead)
):
    return {
        "message": "Profile assigned successfully",
        "status": status.HTTP_201_CREATED,
        "assigned_profile": assign_profile(db, assign_profile_data, current_user)
        }

@router.get("/get_all_profiles",
    response_model=list[ProfileResponse],
    status_code=status.HTTP_200_OK
)
def get_all_profiles_endpoints(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_profiles(db, current_user)

@router.post("/add_list_command_to_profile",
    response_model=ProfileCommandResponse,
    status_code=status.HTTP_201_CREATED
)
def add_list_command(
    command_profile_data: ProfileCommandRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_team_lead)
):
    return add_list_command_to_profile(db, command_profile_data, current_user)
        