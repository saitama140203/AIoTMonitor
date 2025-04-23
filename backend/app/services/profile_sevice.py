from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.profile import Profile, ProfileUser
from app.models.command import Command, CommandProfile
from app.models.user import User
from app.schemas.profile import ProfileCreate, AssignProfile, ProfileCommandRequest, ProfileCommandResponse
from typing import List, Optional, Dict, Any

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
    
def assign_profile(
    db: Session,
    assign_profile_data: AssignProfile,
    current_user: User
) -> ProfileUser:
    try:
        ## Check if the current user has the required role
        if not any(role.role.name in ["team_lead"] for role in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Require Team Lead"
            )
        ## Check if the profile and user exist
        ## and if the user is not already assigned to the profile
        profile = db.query(Profile).filter(Profile.id == assign_profile_data.profile_id).first()
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )

        user = db.query(User).filter(User.id == assign_profile_data.operator_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        ## Check if the user is already assigned to the profile
        exist_profile_user = db.query(ProfileUser).filter(
            ProfileUser.profile_id == assign_profile_data.profile_id,
            ProfileUser.operator_id == assign_profile_data.operator_id
        ).first()

        if exist_profile_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already assigned to this profile"
            )

        profile_user = ProfileUser(
            profile_id = assign_profile_data.profile_id,
            operator_id = assign_profile_data.operator_id
        )
        db.add(profile_user)
        db.commit()
        db.refresh(profile_user)

        return profile_user

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error assigning profile: {str(e)}"
        )

def get_all_profiles(db: Session, current_user: User):
    try:        
        if not any(role.role.name in ("team_lead", "admin") for role in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Require Team Lead Or"
            )        
        
        profiles = db.query(Profile).all()
        return profiles

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching profiles: {str(e)}"
        )
    
def add_list_command_to_profile(
    db: Session,
    request_data: ProfileCommandRequest,
    current_user: User
) -> Dict[str, Any]:
    try:
        # Check if the current user has the required role
        if not any(role.role.name == "team_lead" for role in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Require Team Lead"
            )

        # Check if the profile exists
        profile = db.query(Profile).filter(Profile.id == request_data.profile_id).first()
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )

        # Check if all command_ids exist
        existing_command_ids = {
            cmd.id for cmd in db.query(Command.id).filter(Command.id.in_(request_data.command_ids)).all()
        }

        invalid_ids = set(request_data.command_ids) - existing_command_ids
        if invalid_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid command_ids: {list(invalid_ids)}"
            )

        # Add new command associations
        added_commands = []
        for command_id in request_data.command_ids:
            # Check if already exists
            existing = db.query(CommandProfile).filter_by(
                profile_id=request_data.profile_id,
                command_id=command_id
            ).first()

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Command ID {command_id} is already assigned to this profile"
                )

            new_cp = CommandProfile(
                profile_id=request_data.profile_id,
                command_id=command_id
            )
            db.add(new_cp)
            added_commands.append(command_id)

        db.commit()

        return ProfileCommandResponse(
            command_ids=added_commands,
            profile_id=request_data.profile_id,
            message="Commands added successfully",
            status=status.HTTP_201_CREATED
        )

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding commands to profile: {str(e)}"
        )