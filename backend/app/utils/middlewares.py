# backend/app/utils/middlewares.py
import time
from typing import Callable, Dict, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from jose import jwt
from app.utils.logger import access_logger, log_error
from app.core.config import settings

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware để ghi log tất cả các request và response
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:

        start_time = time.time()
        
        request_id = request.headers.get("X-Request-ID", "-")
        path = request.url.path
        method = request.method
        client_ip = request.client.host if request.client else "unknown"
        
        # Trích xuất thông tin người dùng từ token (nếu có)
        user_info = await self._get_user_from_token(request)
        
        log_data = {
            "request_id": request_id,
            "path": path,
            "method": method,
            "ip": client_ip,
            "user_id": user_info.get("user_id", "-"),
            "username": user_info.get("username", "-")
        }
        
        try:
            response = await call_next(request)
            
            process_time = time.time() - start_time
            
            #log thông tin request và response
            log_data.update({
                "status_code": response.status_code,
                "process_time_ms": round(process_time * 1000, 2)
            })
            

            if response.status_code >= 500:
                access_logger.error(f"Request completed with error", extra=log_data)
            elif response.status_code >= 400:
                access_logger.warning(f"Request completed with client error", extra=log_data)
            else:
                access_logger.info(f"Request completed successfully", extra=log_data)
            
            return response
            
        except Exception as e:
            # Xử lý exception
            process_time = time.time() - start_time
            log_data.update({
                "status_code": 500,
                "process_time_ms": round(process_time * 1000, 2),
                "error": str(e)
            })
            
            # Log lỗi
            log_error(
                error_message=f"Unhandled exception during request processing: {str(e)}",
                module="middleware",
                function="dispatch",
                exception=e,
                user_id=user_info.get("user_id"),
                details=log_data
            )
            
            # Trả về lỗi 500 Internal Server Error
            return Response(
                content={"detail": "Internal server error"},
                status_code=500,
                media_type="application/json"
            )
    
    async def _get_user_from_token(self, request: Request) -> Dict[str, Any]:
        """Trích xuất thông tin người dùng từ JWT token"""
        auth_header = request.headers.get("Authorization", "")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return {}
        
        token = auth_header.replace("Bearer ", "")
        
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return {
                "user_id": payload.get("sub"),
                "username": payload.get("sub"),
                "role": payload.get("role")
            }
        except Exception:
            # Token không hợp lệ hoặc hết hạn
            return {}