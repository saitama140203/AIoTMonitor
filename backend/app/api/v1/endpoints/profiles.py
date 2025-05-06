from fastapi import APIRouter, Depends, status, Query, Path
from sqlalchemy.orm import Session
from app.schemas.profile import ProfileCreate, ProfileResponse, AssignProfile
from app.services.profile_sevice import create_profile, assign_profile, get_all_profiles, get_profile_by_id, get_unassigned_commands, get_unassigned_operators
from app.api.v1.deps import get_db, get_current_team_lead, get_current_user
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

@router.post("/assign_profile")
def assign_profile_operator(
    assign_profile_data: AssignProfile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_team_lead)
):
    return {
        "message": "Profile assigned successfully",
        "code": status.HTTP_201_CREATED,
        "assigned_profile": assign_profile(db, assign_profile_data, current_user)
        }

@router.get("/get_all_profiles"
)
def get_all_profiles_endpoints(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
):
    return get_all_profiles(db, current_user, skip, limit)

@router.get("/get_profile_by_id/{profile_id}"  
)
def get_profile_by_id_ep(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    profile_id: int = Path(..., gt=0),
):
    return get_profile_by_id(db, current_user, profile_id=profile_id)

@router.get("/profiles/{profile_id}/unassigned_operators")
def unassigned_operators_endpoint(
    profile_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_unassigned_operators(db=db, current_user=current_user, profile_id=profile_id)

@router.get("/profiles/{profile_id}/unassigned_commands")
def unassigned_commands_endpoint(
    profile_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_unassigned_commands(db=db, current_user=current_user, profile_id=profile_id)