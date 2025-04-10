# backend/app/utils/logger.py
import logging
import json
import os
import time
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Optional, Dict, Any, Union

# Tạo thư mục logs nếu chưa tồn tại
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

class CustomFormatter(logging.Formatter):
    """
    Lớp formatter tùy chỉnh để hiển thị log màu sắc trong console
    và định dạng JSON cho file log
    """
    
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;20m"
    blue = "\x1b[34;20m"
    reset = "\x1b[0m"
    
    console_format = "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    
    FORMATS = {
        logging.DEBUG: grey + console_format + reset,
        logging.INFO: green + console_format + reset,
        logging.WARNING: yellow + console_format + reset,
        logging.ERROR: red + console_format + reset,
        logging.CRITICAL: bold_red + console_format + reset
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

class JSONFormatter(logging.Formatter):
    """
    Formatter tạo logs dưới định dạng JSON
    """
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        
        if hasattr(record, "user_id"):
            log_record["user_id"] = record.user_id
            
        if hasattr(record, "username"):
            log_record["username"] = record.username
            
        if hasattr(record, "ip"):
            log_record["ip"] = record.ip
            
        if hasattr(record, "action"):
            log_record["action"] = record.action
            
        if hasattr(record, "status"):
            log_record["status"] = record.status
            
        if hasattr(record, "details"):
            log_record["details"] = record.details
        
        return json.dumps(log_record)


def setup_logger(name: str, 
                 log_level: int = logging.INFO, 
                 log_to_console: bool = True,
                 log_to_file: bool = True,
                 log_file: str = None,
                 max_bytes: int = 10 * 1024,  # 10MB
                 backup_count: int = 10):
    """
    Tạo và cấu hình logger với các tùy chọn
    
    Args:
        name: Tên của logger
        log_level: Level logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_console: Ghi log ra console
        log_to_file: Ghi log ra file
        log_file: Tên file log (mặc định: {name}.log)
        max_bytes: Kích thước tối đa của file log trước khi quay vòng
        backup_count: Số lượng file log backup giữ lại
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    if logger.handlers:
        logger.handlers.clear()
    

    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(CustomFormatter())
        logger.addHandler(console_handler)
    
    if log_to_file:
        if not log_file:
            log_file = f"{name}.log"
        
        log_file_path = log_dir / log_file
        
        # File handler với rotating
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)
    
    return logger


app_logger = setup_logger("app", log_file="app.log")
access_logger = setup_logger("access", log_file="access.log")
error_logger = setup_logger("error", log_file="error.log", log_level=logging.ERROR)
audit_logger = setup_logger("audit", log_file="audit.log")
device_logger = setup_logger("device", log_file="device.log")


# def log_user_activity(user_id: Optional[int] = None,
#                      username: Optional[str] = None,
#                      ip: Optional[str] = None,
#                      action: str = None,
#                      status: str = "success",
#                      details: Optional[Dict[str, Any]] = None):
#     """
#     Ghi log hoạt động của người dùng
    
#     Args:
#         user_id: ID của người dùng
#         username: Tên người dùng
#         ip: Địa chỉ IP
#         action: Hành động được thực hiện
#         status: Trạng thái (success/failed/error)
#         details: Chi tiết bổ sung
#     """
#     record = logging.LogRecord(
#         name="audit",
#         level=logging.INFO,
#         pathname="",
#         lineno=0,
#         msg=f"User activity: {action}",
#         args=(),
#         exc_info=None
#     )
    
#     # Thêm thông tin tùy chỉnh
#     if user_id:
#         record.user_id = user_id
#     if username:
#         record.username = username
#     if ip:
#         record.ip = ip
#     if action:
#         record.action = action
#     if status:
#         record.status = status
#     if details:
#         record.details = details
    
#     audit_logger.handle(record)

# # Hàm helper để log hoạt động của thiết bị
# def log_device_activity(device_id: Optional[int] = None,
#                        device_name: Optional[str] = None,
#                        hub_id: Optional[int] = None,
#                        action: str = None,
#                        status: str = "online",
#                        user_id: Optional[int] = None,
#                        details: Optional[Dict[str, Any]] = None):
#     """
#     Ghi log hoạt động của thiết bị
    
#     Args:
#         device_id: ID của thiết bị
#         device_name: Tên của thiết bị
#         hub_id: ID của hub
#         action: Hành động được thực hiện
#         status: Trạng thái thiết bị
#         user_id: Người dùng thực hiện hành động (nếu có)
#         details: Chi tiết bổ sung
#     """
#     record = logging.LogRecord(
#         name="device",
#         level=logging.INFO,
#         pathname="",
#         lineno=0,
#         msg=f"Device activity: {action}",
#         args=(),
#         exc_info=None
#     )
    
#     # Thêm thông tin tùy chỉnh
#     if device_id:
#         record.device_id = device_id
#     if device_name:
#         record.device_name = device_name
#     if hub_id:
#         record.hub_id = hub_id
#     if action:
#         record.action = action
#     if status:
#         record.status = status
#     if user_id:
#         record.user_id = user_id
#     if details:
#         record.details = details
    
#     device_logger.handle(record)

# # Hàm ghi log lỗi với chi tiết mở rộng
# def log_error(error_message: str,
#              module: str = None,
#              function: str = None,
#              exception: Exception = None,
#              user_id: Optional[int] = None,
#              details: Optional[Dict[str, Any]] = None):
#     """
#     Ghi log lỗi với thông tin mở rộng
    
#     Args:
#         error_message: Thông báo lỗi
#         module: Module phát sinh lỗi
#         function: Hàm phát sinh lỗi
#         exception: Exception object
#         user_id: ID người dùng (nếu có)
#         details: Chi tiết bổ sung
#     """
#     extra = {}
#     if module:
#         extra["module"] = module
#     if function:
#         extra["function"] = function
#     if user_id:
#         extra["user_id"] = user_id
#     if details:
#         extra["details"] = details
    
#     if exception:
#         error_logger.exception(error_message, extra=extra)
#     else:
#         error_logger.error(error_message, extra=extra)