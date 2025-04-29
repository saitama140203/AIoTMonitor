# app/services/command_service.py
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.profile import Profile
from app.models.command import Command, CommandProfile
from app.schemas.command import CommandCreate, CommandResponse, CreateCommandList, CommandProfileSchema
from app.models.user import User

def create_command(
    db: Session,
    command_data: CommandCreate,
    current_user: User
) -> CommandResponse:

    try:
        if not any(role.role.name == ("team_lead") for role in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="team_lead role only !!!"
            )

        db_command = Command(
            commands_text=command_data.commands_text,
            description=command_data.description,
            created_by=current_user.id
        )
        
        db.add(db_command)
        db.commit()
        db.refresh(db_command)
        
        return CommandResponse(
            commands_text=db_command.commands_text,
            description=db_command.description
        )

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating command: {str(e)}"
        )
    

def create_command_profiles(
    db: Session,
    data: CreateCommandList,
    current_user: User
) -> Dict[str, Any]:
    try:
        if not any(role.role.name == ("team_lead") for role in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="team_lead role only !!!"
            )

        # Kiểm tra profile có tồn tại không
        profile = db.query(Profile).filter(Profile.id == data.profile_id).first()
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile ID {data.profile_id} not found"
            )

        # Kiểm tra các command_id có hợp lệ không
        existing_commands = db.query(Command.id).filter(Command.id.in_(data.command_ids)).all()
        existing_ids = {cmd.id for cmd in existing_commands}
        missing_ids = set(data.command_ids) - existing_ids
        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Command IDs not found: {list(missing_ids)}"
            )

        existing_links = db.query(CommandProfile.command_id).filter(
            CommandProfile.profile_id == data.profile_id,
            CommandProfile.command_id.in_(data.command_ids)
        ).all()
        if existing_links:              
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Command IDs already linked to this profile"
            )

        new_links = [
            CommandProfile(command_id=cmd_id, profile_id=data.profile_id)
            for cmd_id in data.command_ids
        ]

        db.add_all(new_links)
        db.commit()
        for link in new_links:
            db.refresh(link)

        command_profiles_response: List[CommandProfileSchema] = [
            CommandProfileSchema.from_orm(link) for link in new_links
        ]

        return {
            "message": "Command profiles created successfully",
            "command_profiles": command_profiles_response
        }

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating command-profile links: {str(e)}"
        )
    
def get_all_commands(
    db: Session,
    current_user: User,
    skip: int = 0,
    limit: int = 10,
) -> Dict[str, Any]:
    try:
        if not any(role.role.name == ("team_lead") for role in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="team_lead role only !!!"
            )
        total = db.query(Command).count()
        commands = db.query(Command).offset(skip).limit(limit).all()
        return {
            "message": "Commands fetched successfully",
            "commands": commands,
            "total": total
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching commands: {str(e)}"
        )
    