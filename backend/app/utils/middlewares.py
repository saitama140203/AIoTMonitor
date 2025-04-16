# backend/app/utils/middlewares.py
import time
from typing import Callable, Dict, Any, List
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from jose import jwt
from app.core.config import settings
from app.utils.logger import access_logger, log_error

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware để ghi log tất cả các request và response với hỗ trợ multi-role
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        request_id = request.headers.get("X-Request-ID", "-")
        path = request.url.path
        method = request.method
        client_ip = request.client.host if request.client else "unknown"
        
        user_info = await self._get_user_from_token(request)
        
        log_data = {
            "request_id": request_id,
            "path": path,
            "method": method,
            "ip": client_ip,
            "user_id": user_info.get("user_id", "-"),
            "username": user_info.get("username", "-"),
            "roles": user_info.get("roles", [])
        }
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            log_data.update({
                "status_code": response.status_code,
                "process_time_ms": round(process_time * 1000, 2)
            })
            
            self._log_request(log_data)
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            log_data.update({
                "status_code": 500,
                "process_time_ms": round(process_time * 1000, 2),
                "error": str(e)
            })
            
            self._log_error(log_data, e)
            
            return Response(
                content={"detail": "Internal server error"},
                status_code=500,
                media_type="application/json"
            )
    
    async def _get_user_from_token(self, request: Request) -> Dict[str, Any]:
        """Trích xuất thông tin người dùng từ JWT token với multi-role"""
        auth_header = request.headers.get("Authorization", "")
        
        if not auth_header.startswith("Bearer "):
            return {}
        
        token = auth_header.replace("Bearer ", "")
        
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            return {
                "user_id": payload.get("sub"),
                "username": payload.get("username", ""),
                "roles": payload.get("roles", [])
            }
        except Exception as e:
            log_error(
                error_message=f"Token validation failed: {str(e)}",
                module="middleware",
                function="_get_user_from_token",
                exception=e
            )
            return {}

    def _log_request(self, log_data: Dict[str, Any]):
        """Xử lý logging cho request thành công"""
        if log_data["status_code"] >= 500:
            access_logger.error(
                "Request error", 
                extra=log_data,
                stack_info=True
            )
        elif log_data["status_code"] >= 400:
            access_logger.warning(
                "Client error", 
                extra=log_data
            )
        else:
            access_logger.info(
                "Request success", 
                extra=log_data
            )

    def _log_error(self, log_data: Dict[str, Any], error: Exception):
        """Xử lý logging cho lỗi"""
        log_error(
            error_message=f"Unhandled exception: {str(error)}",
            module="middleware",
            function="dispatch",
            exception=error,
            user_id=log_data.get("user_id"),
            details=log_data
        )
        access_logger.critical(
            "Critical server error", 
            extra=log_data,
            exc_info=True
        )