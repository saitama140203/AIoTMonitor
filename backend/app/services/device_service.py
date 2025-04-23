from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.models.device import Device, Group
from app.models.command import Command, CommandProfile
from app.models.profile import Profile, ProfileUser
from app.models.user import User


from app.schemas.device import (
    DeviceCreate,
    AddDevicesToGroupRequest,
    DeviceResponse,
    GroupCreate,
    GroupResponse,
    DeviceBase
)

def create_device(
    db: Session, 
    device_data: DeviceCreate, 
    current_user: User
) -> DeviceResponse:

    if not any(role.role.name == "team_lead" for role in current_user.roles):
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Yêu cầu quyền Team Lead"
            )

    try:
        existing_device = db.query(Device).filter(Device.mac == device_data.mac).first()
        if existing_device:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Đã tồn tại thiết bị trong hệ thống !!!"
            )
        db_device = Device(
            **device_data.dict(),
            created_by=current_user.id,
            lastseen=datetime.now(),
            status="active",
            group_id=None
        )
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return device_data

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()


def get_devices(
    db: Session,
    current_user: User,
    group_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    mac: Optional[str] = None
) -> List[Device]:
    """
    Lấy danh sách thiết bị (Team Lead/Operator)
    """
    try:
        query = db.query(Device)
        
        user_roles = [role.role.name for role in current_user.roles]

        if "admin" in user_roles or "supervisor" in user_roles:
            pass

        elif "team_lead" in user_roles:
            query = query.filter(Device.created_by == current_user.id)

        # elif "operator" in user_roles:
        #     assigned_profiles = db.query(ProfileUser.profile_id).filter(
        #         ProfileUser.operator_id == current_user.id
        #     ).subquery()

        #     # Lấy tất cả group từ các profile được gán
        #     assigned_groups = db.query(GroupProfile.group_id).filter(
        #         GroupProfile.profile_id.in_(assigned_profiles)
        #     ).distinct().subquery()

        #     # Lọc device thuộc các group được phép truy cập
        #     query = query.filter(Device.group_id.in_(assigned_groups))
        
        if group_id:
            query = query.filter(Device.group_id == group_id)
            
        if status_filter:
            query = query.filter(Device.status == status_filter)

        if mac:
            query = query.filter(Device.mac == mac)    
            
        return query.all()
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi lấy danh sách thiết bị: {str(e)}"
        )

# def update_device_status(
#     db: Session,
#     device_id: int,
#     new_status: str,
#     current_user: User
# ) -> Device:
#     """
#     Cập nhật trạng thái thiết bị (Team Lead only)
#     """
#     try:
#         device = db.query(Device).filter(Device.id == device_id).first()
#         if not device:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Thiết bị không tồn tại"
#             )
            
#         if device.created_by != current_user.id:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Không có quyền cập nhật thiết bị này"
#             )
            
#         device.status = new_status
#         device.lastseen = datetime.now()
        
#         db.commit()
#         db.refresh(device)
#         return device
        
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi cập nhật thiết bị: {str(e)}"
#         )

def create_device_group(
    db: Session,
    group_data: GroupCreate,
    current_user: User
) -> GroupResponse:

    existing_group = db.query(Group).filter(
            Group.name == group_data.name,
        ).first()
        
    if existing_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên nhóm đã tồn tại"
        )
    try:             
        db_group = Group(
            name=group_data.name,
            created_at=datetime.now(),
        )
        
        db.add(db_group)
        db.commit()
        db.refresh(db_group)

        return GroupResponse(
            name=db_group.name,
            created_at=db_group.created_at,
            is_actived=db_group.is_actived
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi tạo nhóm thiết bị: {str(e)}"
        )

def devices_into_group(
    db: Session,
    request_data: AddDevicesToGroupRequest,
    current_user: User
) -> Dict[str, Any]:

    try:
        if not any(role.role.name == "team_lead" for role in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="team_lead role only !!!"
            )

        group = db.query(Group).filter(
            Group.id == request_data.group_id,
        ).first()
        
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found !!!"
            )

        devices = db.query(Device).filter(
            Device.id.in_(request_data.device_ids),
        ).all()

        valid_device_ids = [d.id for d in devices]
        invalid_device_ids = list(set(request_data.device_ids) - set(valid_device_ids))
        
        if invalid_device_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Các thiết bị không hợp lệ: {invalid_device_ids}"
            )

        update_count = db.query(Device).filter(
            Device.id.in_(valid_device_ids)
        ).update(
            {"group_id": request_data.group_id, "lastseen": datetime.now()},
            synchronize_session=False
        )
        
        db.commit()
        
        return {
            "message": "Add devices to group successfully !!!",
            "total_devices": len(valid_device_ids),
            "group_id": request_data.group_id,
            "updated_devices": valid_device_ids
        }

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi cập nhật nhóm: {str(e)}"
        )


