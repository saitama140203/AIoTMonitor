from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.models.device import Device, Group
from app.models.command import Command, CommandProfile
from app.models.profile import Profile, GroupProfile, ProfileUser
from app.models.user import User
from app.schemas.device import (
    DeviceCreate,
    DeviceUpdate,
    GroupCreate,
    CommandCreate,
    ProfileCreate,
    ProfileAssign
)

def create_device(
    db: Session, 
    device_data: DeviceCreate, 
    current_user: User
) -> Device:
    """
    Tạo mới thiết bị (Team Lead only)
    """
    try:
        # Kiểm tra quyền Team Lead
        if not any(role.role.name == "team_lead" for role in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Yêu cầu quyền Team Lead"
            )

        # Kiểm tra group tồn tại
        group = db.query(Group).filter(Group.id == device_data.group_id).first()
        if not group:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nhóm thiết bị không tồn tại"
            )

        # Tạo thiết bị mới
        db_device = Device(
            **device_data.dict(),
            created_by=current_user.id,
            lastseen=datetime.now(),
            status="active"  # Mặc định status khi tạo
        )
        
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi tạo thiết bị: {str(e)}"
        )

def get_devices(
    db: Session,
    current_user: User,
    group_id: Optional[int] = None,
    status_filter: Optional[str] = None
) -> List[Device]:
    """
    Lấy danh sách thiết bị (Team Lead/Operator)
    """
    try:
        query = db.query(Device)
        
        # Team Lead chỉ xem thiết bị của nhóm mình
        if any(role.role.name == "team_lead" for role in current_user.roles):
            query = query.filter(Device.created_by == current_user.id)
        
        # Operator chỉ xem thiết bị được assign
        elif any(role.role.name == "operator" for role in current_user.roles):
            # Logic lấy thiết bị từ profile được assign
            pass
        
        if group_id:
            query = query.filter(Device.group_id == group_id)
            
        if status_filter:
            query = query.filter(Device.status == status_filter)
            
        return query.all()
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi lấy danh sách thiết bị: {str(e)}"
        )

def update_device_status(
    db: Session,
    device_id: int,
    new_status: str,
    current_user: User
) -> Device:
    """
    Cập nhật trạng thái thiết bị (Team Lead only)
    """
    try:
        device = db.query(Device).filter(Device.id == device_id).first()
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Thiết bị không tồn tại"
            )
            
        if device.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Không có quyền cập nhật thiết bị này"
            )
            
        device.status = new_status
        device.lastseen = datetime.now()
        
        db.commit()
        db.refresh(device)
        return device
        
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi cập nhật thiết bị: {str(e)}"
        )

def create_device_group(
    db: Session,
    group_data: GroupCreate,
    current_user: User
) -> Group:
    """
    Tạo nhóm thiết bị mới (Team Lead only)
    """
    try:
        existing_group = db.query(Group).filter(
            Group.name == group_data.name,
            Group.created_by == current_user.id
        ).first()
        
        if existing_group:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tên nhóm đã tồn tại"
            )
            
        db_group = Group(
            **group_data.dict(),
            created_by=current_user.id
        )
        
        db.add(db_group)
        db.commit()
        db.refresh(db_group)
        return db_group
        
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi tạo nhóm thiết bị: {str(e)}"
        )

def create_command_list(
    db: Session,
    command_data: CommandCreate,
    current_user: User
) -> Command:
    """
    Tạo command mới (Team Lead only)
    """
    try:
        db_command = Command(
            **command_data.dict(),
            created_by=current_user.id
        )
        
        db.add(db_command)
        db.commit()
        db.refresh(db_command)
        return db_command
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi tạo command: {str(e)}"
        )

def create_profile(
    db: Session,
    profile_data: ProfileCreate,
    current_user: User
) -> Profile:
    """
    Tạo profile mới (Team Lead only)
    """
    try:
        # Kiểm tra tồn tại command list và device group
        command_group = db.query(Command).filter(
            Command.id == profile_data.command_list_id,
            Command.created_by == current_user.id
        ).first()
        
        device_group = db.query(Group).filter(
            Group.id == profile_data.device_group_id,
            Group.created_by == current_user.id
        ).first()
        
        if not command_group or not device_group:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Command list hoặc device group không hợp lệ"
            )
            
        # Tạo profile
        db_profile = Profile(
            name=profile_data.name,
            created_by=current_user.id
        )
        db.add(db_profile)
        db.flush()
        
        # Liên kết command list
        db.add(CommandProfile(
            profile_id=db_profile.id,
            command_id=profile_data.command_list_id
        ))
        
        # Liên kết device group
        db.add(GroupProfile(
            profile_id=db_profile.id,
            group_id=profile_data.device_group_id
        ))
        
        db.commit()
        return db_profile
        
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi tạo profile: {str(e)}"
        )

def assign_profile_to_operator(
    db: Session,
    profile_assign: ProfileAssign,
    current_user: User
) -> Dict[str, Any]:
    """
    Gán profile cho operator (Team Lead only)
    """
    try:
        # Kiểm tra profile thuộc về Team Lead
        profile = db.query(Profile).filter(
            Profile.id == profile_assign.profile_id,
            Profile.created_by == current_user.id
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile không tồn tại"
            )
            
        # Kiểm tra operator
        operator = db.query(User).filter(
            User.id == profile_assign.operator_id,
            User.is_active == True
        ).first()
        
        if not operator or not any(role.role.name == "operator" for role in operator.roles):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Operator không hợp lệ"
            )
            
        # Tạo liên kết
        db_assignment = ProfileUser(
            profile_id=profile.id,
            operator_id=operator.id
        )
        
        db.add(db_assignment)
        db.commit()
        
        return {
            "message": "Gán profile thành công",
            "profile_id": profile.id,
            "operator_id": operator.id
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi gán profile: {str(e)}"
        )