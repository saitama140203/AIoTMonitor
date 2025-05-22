from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.supervisor import SessionDetail, TerminateSessionRequest
from app.services.supervisor import SupervisorService
from app.schemas.supervisor import SessionHistoryItem
from app.api.v1.deps import get_db, get_current_supervisor
from app.models import User

router = APIRouter()

@router.get("/sessions/active", response_model=list[SessionDetail])
def list_active_sessions(
    db: Session = Depends(get_db),
    _ = Depends(get_current_supervisor)  # Auth check
):
    try:
        return SupervisorService.get_active_sessions(db)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post("/sessions/{session_id}/terminate")
def terminate_session(
    session_id: int,
    request: TerminateSessionRequest,
    db: Session = Depends(get_db),
    supervisor: User = Depends(get_current_supervisor)
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