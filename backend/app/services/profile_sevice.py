from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from typing import List, Dict, Any
from app.models import Profile, Command
from app.models.device import Device, Group
from app.models.user import User, UserRole
from app.models.profile import ProfileUser
from app.schemas.profile import ProfileCreate, AssignProfile, AssignProfileResponse
from app.models.command import CommandProfile
from app.models.session import Session as SessionModal

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
) -> AssignProfileResponse:
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
        db.flush()
        
        # Lấy device group của profile
        device_group = db.query(Group).filter(Group.id == profile.group_id).first()
        if not device_group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device group not found for this profile"
            )
        
        devices = db.query(Device).filter(Device.group_id == device_group.id).all()
        if not devices:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No devices found in this device group"
            )
        
        # Tạo sessions cho từng thiết bị
        session_ids = []
        for device in devices:
            session = SessionModal(
                operator_id=assign_profile_data.operator_id,
                device_id=device.id,
                status="active"
            )
            db.add(session)
            db.flush()
            session_ids.append(session.id)

        db.commit()
        db.refresh(profile_user)
        
        return AssignProfileResponse(
            profile_id=profile_user.profile_id,
            operator_id=profile_user.operator_id,
            session_ids=session_ids
        )

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error assigning profile: {str(e)}"
        )
    
def get_all_profiles(
        db: Session,
        current_user: User,
        skip: int = 0,
        limit: int = 10,
):
    try:        
        if not any(role.role.name in ("team_lead", "admin") for role in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Require Team Lead Or Admin"
            )        
        
        profiles = db.query(Profile).offset(skip).limit(limit).all()
        total_profiles = db.query(Profile).count()
        return {
            "message": "Profiles retrieved successfully",
            "code": status.HTTP_200_OK,
            "total": total_profiles,
            "skip": skip,
            "limit": limit,
            "data": profiles
        }

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching profiles: {str(e)}"
        )
    
def get_profile_by_id(
        db: Session,
        current_user: User,
        profile_id: int
) -> Dict[str, Any]:
    try:
        if not any(role.role.name in ("team_lead") for role in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Require Team Lead"
            )        

        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return {"error": "Profile not found"}

        operators: List[Dict[str, Any]] = [            
                pu.user.username            
            for pu in profile.profile_users
        ]

        commands: List[Dict[str, Any]] = [
                cp.command.commands_text
            for cp in profile.command_profiles
        ]

        return {
            "code": status.HTTP_200_OK,
            "message": "Get profile successfully",
            "data": {
                "name": profile.name,
                "operators": operators,
                "commands": commands
            }
        }

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching profile: {str(e)}"
        )
    
def get_unassigned_operators(
    db: Session,
    current_user: User,
    profile_id: int
) -> Dict[str, Any]:
    if not any(role.role.name == "team_lead" for role in current_user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Require Team Lead"
        )

    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    assigned_operator_ids = [pu.operator_id for pu in profile.profile_users]

    unassigned_users = (
        db.query(User)
        .options(joinedload(User.roles).joinedload(UserRole.role))
        .filter(User.id.notin_(assigned_operator_ids))
        .all()
    )

    operators_only = [
        user for user in unassigned_users
        if any(user_role.role.name == "operator" for user_role in user.roles)
    ]

    if not operators_only:        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No unassigned operators found"
        )

    return {
        "code": status.HTTP_200_OK,
        "message": "Get unassigned operators successfully",
        "data": [
            {"id": user.id, "username": user.username, "full_name": user.full_name}
            for user in operators_only
        ]
    }

def get_unassigned_commands(
    db: Session,
    current_user: User,
    profile_id: int
) -> Dict[str, Any]:
    if not any(role.role.name == "team_lead" for role in current_user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Require Team Lead"
        )

    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    assigned_command_ids = [cp.command_id for cp in profile.command_profiles]

    unassigned_commands = db.query(Command).filter(Command.id.notin_(assigned_command_ids)).all()

    if not unassigned_commands:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No unassigned commands found"
        )

    return {
        "code": status.HTTP_200_OK,
        "message": "Get unassigned commands successfully",
        "data": [
            {
                "id": cmd.id,
                "commands_text": cmd.commands_text,
                "description": cmd.description
            }
            for cmd in unassigned_commands
        ]
    }



def get_resources(
    profile_id: int,
    db: Session,
    current_user: User,
    skip: int = 0,
    limit: int = 10
) -> Dict[str, Any]:


    # 2. Lấy profile
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy profile với id: {profile_id}",
        )

    # 3. Commands theo profile (phân trang)
    cmd_q = (
        db.query(Command)
        .join(CommandProfile, CommandProfile.command_id == Command.id)
        .filter(CommandProfile.profile_id == profile_id)
    )
    total_commands = cmd_q.count()
    commands = cmd_q.offset(skip).limit(limit).all()

    # 4. Devices trong group của profile (nếu có)
    total_devices = 0
    devices = []
    if profile.group_id:
        dev_q = db.query(Device).filter(Device.group_id == profile.group_id)
        total_devices = dev_q.count()
        devices = dev_q.offset(skip).limit(limit).all()

    # 5. Operators gán với profile
    op_q = (
        db.query(User)
        .join(ProfileUser, ProfileUser.operator_id == User.id)
        .filter(ProfileUser.profile_id == profile_id)
    )
    total_operators = op_q.count()
    operators = op_q.offset(skip).limit(limit).all()

    # 6. Trả về kết quả
    return {
        "profile": {
            "id": profile.id,
            "name": profile.name,
            "created_at": profile.created_at,
            "group_id": profile.group_id,
            "group_name": profile.group.name if profile.group else None,
        },
        "commands": {
            "total": total_commands,
            "skip": skip,
            "limit": limit,
            "items": [
                {
                    "id": c.id,
                    "commands_text": c.commands_text,
                    "description": c.description,
                    "created_by": c.created_by,
                }
                for c in commands
            ],
        },
        "devices": {
            "total": total_devices,
            "skip": skip,
            "limit": limit,
            "items": [
                {
                    "id": d.id,
                    "name": d.name,
                    "ip": d.ip,
                    "port": d.port,
                    "status": d.status,
                    "platform": d.platform,
                    "lastseen": d.lastseen,
                }
                for d in devices
            ],
        },
        "operators": {
            "total": total_operators,
            "skip": skip,
            "limit": limit,
            "items": [
                {
                    "id": o.id,
                    "email": o.email,
                    "full_name": o.full_name,
                }
                for o in operators
            ],
        },
    }



def get_list_profile_by_operator(
        db: Session,
        current_user: User,
        skip: int = 0,
        limit: int = 10,
):
    try:
        # Lấy tất cả profile được liên kết với current_user qua ProfileUser
        profiles_query = (
            db.query(Profile)
            .join(ProfileUser, ProfileUser.profile_id == Profile.id)
            .filter(ProfileUser.operator_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )

        total_profiles = (
            db.query(Profile)
            .join(ProfileUser, ProfileUser.profile_id == Profile.id)
            .filter(ProfileUser.operator_id == current_user.id)
            .count()
        )

        profiles = profiles_query.all()

        return {
            "message": "Profiles retrieved successfully",
            "code": status.HTTP_200_OK,
            "total": total_profiles,
            "skip": skip,
            "limit": limit,
            "data": profiles
        }

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching profiles: {str(e)}"
        )
