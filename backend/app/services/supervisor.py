from sqlalchemy.orm import Session as DBSession, joinedload
from sqlalchemy.sql import func
from typing import List
from datetime import datetime

from app.models import  User, Device
from app.models.session import Session,SessionHistory
from app.schemas.supervisor import (
    SessionDetail,
    TerminateSessionRequest,
    SessionHistoryItem
)

class SupervisorService:
    @staticmethod
    def get_active_sessions(db: DBSession) -> List[SessionDetail]:
        sessions = db.query(Session)\
            .options(joinedload(Session.operator), joinedload(Session.device))\
            .filter(Session.status == "active")\
            .all()
        
        return [
            SessionDetail(
                session_id=session.id,
                operator_name=session.operator.username,
                device_name=session.device.name,
                status=session.status,
                start_time=session.start_time,
                current_command=session.current_command
            ) for session in sessions
        ]

    @staticmethod
    def terminate_session(db: DBSession, session_id: int, request: TerminateSessionRequest):
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError("Session not found")

        if session.status == "terminated":
            raise ValueError("Session already terminated")

        session.status = "terminated"
        session.end_time = datetime.utcnow()

        history = SessionHistory(
            session_id=session_id,
            terminated_by=request.terminated_by,
            end_status="killed"
        )

        db.add(history)
        db.commit()
        db.refresh(session)

    @staticmethod
    def get_session_history(db: DBSession) -> List[SessionHistoryItem]:
        histories = db.query(SessionHistory)\
            .options(joinedload(SessionHistory.session).joinedload(Session.device))\
            .all()

        return [
            SessionHistoryItem(
                session_id=history.session_id,
                device_name=history.session.device.name,
                end_status=history.end_status,
                ended_at=history.created_at
            ) for history in histories
        ]
