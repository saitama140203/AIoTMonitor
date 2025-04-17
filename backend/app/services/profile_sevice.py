from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Profile
from app.models.user import User
from app.schemas.profile import ProfileCreate

def create_profile(
    db: Session,
    profile_data: ProfileCreate,
    current_user: User
) -> Profile:
    try:
        if not any(role.role.name in ["team_lead"] for role in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Require Team Lead"
            )

        existing_profile = db.query(Profile).filter(
            Profile.name == profile_data.name
        ).first()
        
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Profile name already exists"
            )

        new_profile = Profile(
            name=profile_data.name,
            group_id=profile_data.group_id,
        )
        
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        
        return new_profile

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating profile: {str(e)}"
        )
