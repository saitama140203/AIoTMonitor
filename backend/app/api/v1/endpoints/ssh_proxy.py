import asyncio
import threading
import json
from contextlib import suppress
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import paramiko

router = APIRouter()

@router.websocket("/ssh")
async def ssh_ws(ws: WebSocket):
    await ws.accept()

    # 1. Nhận config từ client
    cfg = await ws.receive_json()
    host = cfg["host"]
    port = cfg.get("port", 22)
    username = cfg["username"]
    password = cfg["password"]

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
                        loop.call_soon_threadsafe(asyncio.create_task, ws.send_text(data.decode(errors="ignore")))
                else:
                    # Giảm tải CPU
                    import time; time.sleep(0.01)
        except Exception:
            pass

    t = threading.Thread(target=read_ssh, daemon=True)
    t.start()

    # 5. Xử lý dữ liệu từ FE
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
            chan.send(msg)
    except WebSocketDisconnect:
        pass
    finally:
        stop_event.set()
        chan.close()
        client.close()
        with suppress(Exception):
            await ws.close()
