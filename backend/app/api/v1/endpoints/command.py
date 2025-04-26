# app/api/v1/endpoints/commands.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from typing import List, Any, Dict
from app.services.command_service import create_command, create_command_profiles
from app.schemas.command import CommandCreate, CommandResponse, CreateCommandList
from app.api.v1.deps import get_db, get_current_team_lead, get_current_user

router = APIRouter()

@router.post("/create_command", response_model=CommandResponse)
def teamlead_create_command(
    command_data: CommandCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_team_lead)
):
    return create_command(db, command_data, current_user)

@router.post("/command-profiles/", response_model=Dict[str, Any])
def create_command_profiles_endpoint(
    data: CreateCommandList,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_team_lead)
):
    return create_command_profiles(db, data, current_user)
