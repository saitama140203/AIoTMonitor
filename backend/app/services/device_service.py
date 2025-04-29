from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.models.device import Device, Group
from app.models.profile import ProfileUser, Profile
from app.models.user import User
from app.core.security import get_password_hash


from app.schemas.device import (
    DeviceCreate,
    AddDevicesToGroupRequest,
    DeviceResponse,
    GroupCreate,
    GroupResponse
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
        # existing_device = db.query(Device).filter(Device.username == device_data.username).first()
        # if existing_device:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Username Đã tồn tại thiết bị trong hệ thống !!!"
        #     )
        ip_address = str(device_data.ip)
        existing_device = db.query(Device).filter(Device.ip == ip_address).first()
        if existing_device:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Địa chỉ IP này đã tồn tại thiết bị trong hệ thống !!!"
            )
        
        password_hash = get_password_hash(device_data.password)

        db_device = Device(
            name=device_data.name,
            username=device_data.username,
            ip=ip_address,
            port=device_data.port,
            hashed_password=password_hash,
            platform=device_data.platform,
            created_by=current_user.id,
            lastseen=datetime.now(),
            status="active",
            group_id=None
        )
        db.add(db_device)
        db.commit()
        db.refresh(db_device)        
        return DeviceResponse.model_validate(device_data)
    
    except HTTPException as e:
        db.rollback()
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
    status_filter: Optional[str] = None,
    username: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
):
    try:
        query = db.query(Device)
        
        user_roles = [role.role.name for role in current_user.roles]

        if "admin" in user_roles or "supervisor" in user_roles:
            pass

        elif "team_lead" in user_roles:
            query = query.filter(Device.created_by == current_user.id)

        elif "operator" in user_roles:
            assigned_profiles = db.query(ProfileUser.profile_id).filter(
                ProfileUser.operator_id == current_user.id
            ).subquery()

            # Lấy tất cả group từ các profile được gán
            assigned_groups = db.query(Profile.group_id).filter(
                Profile.id.in_(assigned_profiles)
            ).distinct().subquery()

            # Lọc device thuộc các group được phép truy cập
            query = query.filter(Device.group_id.in_(assigned_groups))
        
        if group_id:
            query = query.filter(Device.group_id == group_id)
            
        if status_filter:
            query = query.filter(Device.status == status_filter)

        if username:
            query = query.filter(Device.username == username)    

        total = query.count()    
        query = query.offset(skip).limit(limit).all()
        return {
            "message": "Lấy danh sách thiết bị thành công",
            "code": status.HTTP_200_OK,
            "data": query,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    
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


def get_all_groups(
    db: Session,
    current_user: User,
    skip: int = 0,
    limit: int = 10
) -> Dict[str, Any]:
    try:
        if not any(role.role.name == ("team_lead") for role in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="team_lead role only !!!"
            )
        total = db.query(Group).count()
        groups = db.query(Group).offset(skip).limit(limit).all()
        return {
            "message": "Lấy danh sách nhóm thiết bị thành công",
            "code": status.HTTP_200_OK,
            "data": groups,
            "total": total,
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi lấy danh sách nhóm thiết bị: {str(e)}"
        )