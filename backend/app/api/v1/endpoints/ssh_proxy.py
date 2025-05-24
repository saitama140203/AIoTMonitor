import asyncio
import threading
import json
from contextlib import suppress
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import paramiko
from app.services.supervisor import SupervisorService
from app.models.session import Session as SessionModel
from app.api.v1.deps import get_db
from fastapi import Depends
from sqlalchemy.orm import Session as DBSession

router = APIRouter()

# class OperatorConnectionManager:
#     def __init__(self):
#         self.connections: dict[str, WebSocket] = {}  # Lưu theo session_id

#     async def connect(self, session_id: str, ws: WebSocket):
#         await ws.accept()
#         self.connections[session_id] = ws

#     def disconnect(self, session_id: str):
#         with suppress(Exception):
#             self.connections.pop(session_id, None)

#     async def send_terminate(self, session_id: str):
#         ws = self.connections.get(session_id)
#         if ws:
#             try:
#                 await ws.send_json({"type": "terminate"})
#             except Exception:
#                 self.disconnect(session_id)

# # Khởi tạo global instance
# operator_manager = OperatorConnectionManager()

class SupervisorConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        with suppress(Exception):
            self.connections.remove(ws)

    async def broadcast(self, data: dict):
        for ws in self.connections:
            try:
                await ws.send_json(data)
            except Exception:
                self.disconnect(ws)

supervisor_manager = SupervisorConnectionManager()

# =================== Supervisor WebSocket ===========================
@router.websocket("/supervisor")
async def supervisor_ws(ws: WebSocket):
    await supervisor_manager.connect(ws)
    try:
        while True:
            await ws.receive_text()  # Giữ kết nối supervisor (ping/pong)
    except WebSocketDisconnect:
        supervisor_manager.disconnect(ws)

# ================= SSH WebSocket Handler =============================
@router.websocket("/ssh")
async def ssh_ws(ws: WebSocket):
    await ws.accept()

    # 1. Nhận config từ client
    cfg = await ws.receive_json()
    host = cfg["host"]
    port = cfg.get("port", 22)
    username = cfg["username"]
    password = cfg["password"]
    session_id = cfg.get("session_id")

    if session_id:
        try:
            db = next(get_db())
            session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if session and session.status == "terminated":
                session.status = "active"
                db.commit()
        except Exception as e:
            print(f"Failed to update session status to active: {e}")

    await supervisor_manager.broadcast({
        "type": "session_connected",
        "session_id": session_id
    })

    # 2. Kết nối SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, port=port, username=username, password=password, look_for_keys=False, allow_agent=False)
    except Exception as e:
        await ws.send_text(f"\r\n*** SSH connection failed: {e}\r\n")
        with suppress(Exception): await ws.close()
        return

    # 3. Tạo PTY shell, mặc định 80x24
    chan = client.get_transport().open_session()
    cols, rows = 80, 24
    chan.get_pty(term="xterm", width=cols, height=rows)
    chan.invoke_shell()

    loop = asyncio.get_event_loop()
    stop_event = threading.Event()

    # 4. Thread đọc SSH -> WebSocket
    def read_ssh():
        try:
            while not stop_event.is_set():
                if chan.recv_ready():
                    data = chan.recv(4096)
                    if data:
                        text = data.decode(errors="ignore")
                        # Gửi cho operator (gốc)
                        loop.call_soon_threadsafe(asyncio.create_task, ws.send_text(text))
                        # Gửi cho tất cả supervisor
                        loop.call_soon_threadsafe(asyncio.create_task, supervisor_manager.broadcast({
                            "type": "ssh_output",
                            "text": text,
                            "session_id": session_id
                        }))
                        # loop.call_soon_threadsafe(asyncio.create_task, ws.send_text(data.decode(errors="ignore")))
                else:
                    # Giảm tải CPU
                    import time; time.sleep(0.01)
        except Exception:
            pass

    t = threading.Thread(target=read_ssh, daemon=True)
    t.start()

    # 5. Task kiểm tra trạng thái session định kỳ ( mỗi 2s )
    async def check_session_status():
        while not stop_event.is_set():
            await asyncio.sleep(2) 
            db = next(get_db())
            session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if not session or session.status == "terminated":
                # Gửi lệnh terminate
                try:
                    await ws.send_json({"type": "terminate"})
                except:
                    pass
                # Đóng kết nối SSH + WebSocket
                chan.close()
                client.close()
                await ws.close()
                break

    # Khởi chạy task kiểm tra trạng thái session
    check_task = asyncio.create_task(check_session_status())

    # 6. Xử lý dữ liệu từ FE
    current_command = ""
    try:
        while True:
            msg = await ws.receive_text()
            # --- Nhận sự kiện resize ---
            try:
                data = json.loads(msg)
                if isinstance(data, dict) and data.get("type") == "resize":
                    cols = int(data.get("cols", 80))
                    rows = int(data.get("rows", 24))
                    chan.resize_pty(width=cols, height=rows)
                    continue
            except Exception:
                pass
            # --- Forward tất cả input xuống SSH ---
            if msg == "\r":
                    # Cập nhật vào DB
                try:
                    db = next(get_db())  # Lấy session DB
                    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
                    if session:
                        session.current_command = current_command
                        db.commit()
                except Exception as e:
                    print("Failed to update current_command in DB:", e)

                # Gửi cho supervisor
                await supervisor_manager.broadcast({
                    "type": "current_command",
                    "current_command": current_command,
                    "session_id": session_id
                })
                current_command = ""
            else:
                current_command += msg
            # Forward input to SSH
            chan.send(msg)

    except WebSocketDisconnect:
        pass
    finally:
        check_task.cancel()
        stop_event.set()
        chan.close()
        client.close()
        with suppress(Exception):
            await ws.close()
