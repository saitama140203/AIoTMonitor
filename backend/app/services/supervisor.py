from sqlalchemy.orm import Session as DBSession, joinedload
from sqlalchemy.sql import func
from typing import List
from datetime import datetime

from app.models import  User, Device
from app.models.session import Session as SessionModal,SessionHistory
from app.schemas.supervisor import (
    SessionDetail,
    TerminateSessionRequest,
    SessionHistoryItem
)
from app.models.session import Session,SessionCommand
from datetime import timedelta
from datetime import timezone

class SupervisorService:
    @staticmethod
    def create_session(db, operator_id, device_id):
        new_session = Session(
            operator_id=operator_id,
            device_id=device_id,
            status="active"
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session) 
        return new_session
    
    @staticmethod
    def get_active_sessions(db: DBSession) -> List[SessionDetail]:
        sessions = db.query(SessionModal)\
            .options(joinedload(SessionModal.operator), joinedload(SessionModal.device))\
            .filter(SessionModal.status == "active")\
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
        session = db.query(SessionModal).filter(SessionModal.id == session_id).first()
        if not session:
            raise ValueError("Session not found")

        if session.status == "terminated":
            raise ValueError("Session already terminated")

        try:
            session.status = "terminated"
            session.end_time = datetime.utcnow()
            db.commit()
            db.refresh(session)
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def get_session_history(db: DBSession) -> List[SessionHistoryItem]:
        def ensure_aware(dt):
            if dt is None:
                return None
            if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt

        sessions = db.query(SessionModal)\
            .options(
                joinedload(SessionModal.device),
                joinedload(SessionModal.operator)
            )\
            .order_by(SessionModal.start_time.desc())\
            .all()

        result = []
        for session in sessions:
            all_commands = db.query(SessionCommand)\
                .filter(SessionCommand.session_id == session.id)\
                .order_by(SessionCommand.timestamp.asc())\
                .all()

            ended_at_aware = ensure_aware(session.end_time)
            connected_time_aware = ensure_aware(session.connected_time)

            duration = None
            if ended_at_aware and connected_time_aware:
                duration = (ended_at_aware - connected_time_aware).total_seconds()

            result.append(SessionHistoryItem(
                session_id=session.id,
                device_name=session.device.name,
                operator_name=session.operator.username,
                end_status=session.status,
                ended_at=ended_at_aware,
                connected_time=connected_time_aware,
                duration=duration,
                last_commands=[
                    {"text": cmd.command_text, "timestamp": cmd.timestamp}
                    for cmd in all_commands[-5:]
                ],
                all_commands=[
                    {"text": cmd.command_text, "timestamp": cmd.timestamp}
                    for cmd in all_commands
                ]
            ))

        return result


    # @staticmethod
    # def get_session_history(db: DBSession) -> List[SessionHistoryItem]:
    #     histories = db.query(SessionHistory)\
    #         .options(
    #             joinedload(SessionHistory.session)
    #             .joinedload(SessionModal.device),
    #             joinedload(SessionHistory.session)
    #             .joinedload(SessionModal.operator)
    #         )\
    #         .all()

    #     result = []
    #     for history in histories:
    #         all_commands = db.query(SessionCommand)\
    #             .filter(SessionCommand.session_id == history.session_id)\
    #             .order_by(SessionCommand.timestamp.asc())\
    #             .all()

    #         result.append(SessionHistoryItem(
    #             session_id=history.session_id,
    #             device_name=history.session.device.name,
    #             operator_name=history.session.operator.username,
    #             end_status=history.end_status,
    #             ended_at=history.created_at,
    #             connected_time=history.connected_time,
    #             last_commands=[
    #                 {"text": cmd.command_text, "timestamp": cmd.timestamp}
    #                 for cmd in all_commands[-5:] 
    #             ],
    #             all_commands=[
    #                 {"text": cmd.command_text, "timestamp": cmd.timestamp}
    #                 for cmd in all_commands
    #             ]
    #         ))

    #     return result
    
    @staticmethod
    def get_active_session_by_operator_and_device(
        db: DBSession,
        operator_id: int,
        device_id: int
    ) -> Session:
        return db.query(SessionModal)\
            .filter(
                SessionModal.operator_id == operator_id,
                SessionModal.device_id == device_id,
                SessionModal.status.in_(["active", "terminated"])
            )\
            .order_by(SessionModal.start_time.desc())\
            .first()
    @staticmethod
    def save_command_to_session(db, session_id: int, command_text: str):
        new_command = SessionCommand(
            session_id=session_id,
            command_text=command_text,
            timestamp=datetime.utcnow()
        )
        db.add(new_command)
        db.commit()
        db.refresh(new_command)
        return new_command
