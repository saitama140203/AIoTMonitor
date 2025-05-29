from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.supervisor import SessionDetail, TerminateSessionRequest
from app.services.supervisor import SupervisorService
from app.schemas.supervisor import SessionHistoryItem
from app.api.v1.deps import get_db, get_current_supervisor,get_current_user
from app.models import User
from app.models.session import Session as SessionModal
from app.models.session import SessionCommand
from fastapi import Query
from datetime import datetime
from app.schemas.supervisor import SessionCreateSchema
from app.schemas.supervisor import CommandCreate

router = APIRouter()

@router.post("/sessions", summary="Create new SSH session")
def create_session(
    session_in: SessionCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Tạo session mới
    new_session = SessionModal(
        operator_id=session_in.operator_id,
        device_id=session_in.device_id,
        status="active",
        start_time=datetime.utcnow()
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {"session_id": new_session.id, "message": "Session created"}
# @router.post("/sessions")
# def start_session(operator_id: int, device_id: int, db: Session = Depends(get_db)):
#     session = SupervisorService.create_session(db, operator_id, device_id)
#     return {"session_id": session.id}

@router.get("/sessions/active", response_model=list[SessionDetail])
def list_active_sessions(
    db: Session = Depends(get_db),
    _ = Depends(get_current_supervisor)  # Auth check
):
    try:
        return SupervisorService.get_active_sessions(db)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/sessions", summary="Get active session by operator and device")
def get_active_session(
    operator_id: int,
    device_id: int,
    db: Session = Depends(get_db)
):
    session = SupervisorService.get_active_session_by_operator_and_device(
        db=db,
        operator_id=operator_id,
        device_id=device_id
    )

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"session_id": session.id}
    
@router.post("/sessions/{session_id}/terminate")
def terminate_session(
    session_id: int,
    request: TerminateSessionRequest,
    db: Session = Depends(get_db),
    _= Depends(get_current_supervisor)
):
    try:
        SupervisorService.terminate_session(db, session_id, request)
        return {"message": "Session terminated"}
    except ValueError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
    
@router.get("/sessions/history", response_model=list[SessionHistoryItem])
def list_session_history(
    db: Session = Depends(get_db),
    _ = Depends(get_current_supervisor)
):
    try:
        return SupervisorService.get_session_history(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/sessions/{session_id}/connect", summary="Mark session as connected (SSH started)")
def mark_connected_time(
    session_id: int,
    db: Session = Depends(get_db),
    _= Depends(get_current_user) 
):
    session = db.query(SessionModal).filter(SessionModal.id == session_id).first()
    if not session:
        raise HTTPException(404, "Session not found")

    session.connected_time = datetime.utcnow()
    db.commit()
    return {"message": "Connected time recorded"}

from fastapi import Depends, HTTPException

@router.get("/sessions/{session_id}/commands")
def get_session_commands(session_id: int, db=Depends(get_db)):
    commands = db.query(SessionCommand).filter(SessionCommand.session_id == session_id).order_by(SessionCommand.timestamp).all()
    if not commands:
        raise HTTPException(status_code=404, detail="No commands found for this session")

    return {
        "session_id": session_id,
        "commands": [
            {"command_text": c.command_text, "timestamp": c.timestamp.isoformat()}
            for c in commands
        ]
    }


@router.post("/execute-command/")
async def execute_command(cmd_req: CommandCreate, db: Session = Depends(get_db)):
    session_id = cmd_req.session_id
    command_text = cmd_req.command_text
    
    SupervisorService.save_command_to_session(db, session_id, command_text)

    output = f"Executed: {command_text}"

    return {"status": "success", "output": output}
