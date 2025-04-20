from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Profile
from app.models.user import User
from app.schemas.profile import ProfileCreate
from app.models.profile import ProfileUser

class ProfileService:
    def __init__(self, db: Session):
        self.db = db

    def create_profile(
        self,
        profile_data: ProfileCreate,
        current_user: User
    ) -> Profile:
        try:
            if not any(role.role.name in ["team_lead"] for role in current_user.roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Require Team Lead"
                )

            existing_profile = self.db.query(Profile).filter(
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
            
            self.db.add(new_profile)
            self.db.commit()
            self.db.refresh(new_profile)
            
            return new_profile

        except HTTPException as e:
            self.db.rollback()
            raise e
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating profile: {str(e)}"
            )

    def assign_profile_to_operator(
        self,
        profile_id: int,
        operator_id: int,
        current_user: User
    ) -> dict:
        try:
            if not any(role.role.name in ["team_lead"] for role in current_user.roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Require Team Lead"
                )

            profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )

            operator = self.db.query(User).filter(User.id == operator_id).first()
            if not operator:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Operator not found"
                )

            existing_assignment = self.db.query(ProfileUser).filter(
                ProfileUser.profile_id == profile_id,
                ProfileUser.operator_id == operator_id
            ).first()

            if existing_assignment:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Profile already assigned to this operator"
                )

            new_assignment = ProfileUser(
                profile_id=profile_id,
                operator_id=operator_id
            )
            
            self.db.add(new_assignment)
            self.db.commit()
            
            return {"message": "Profile assigned to operator successfully"}

        except HTTPException as e:
            self.db.rollback()
            raise e
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error assigning profile to operator: {str(e)}"
            )
