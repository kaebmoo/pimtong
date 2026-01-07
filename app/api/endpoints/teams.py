from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.core.database import get_db
from app.models.models import Team, User, UserRole
from pydantic import BaseModel

router = APIRouter()

class TeamBase(BaseModel):
    name: str
    color: str = "#0ea5e9"

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    pass

class MemberOut(BaseModel):
    id: int
    full_name: str
    username: str
    class Config:
        from_attributes = True

class TeamOut(TeamBase):
    id: int
    member_count: int = 0
    members: List[MemberOut] = []
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[TeamOut])
def read_teams(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    teams = db.query(Team).all()
    # Manual mapping to include member count efficiently
    results = []
    for t in teams:
        t_out = TeamOut.from_orm(t)
        t_out.member_count = len(t.members)
        # Populate members
        t_out.members = [MemberOut.from_orm(m) for m in t.members]
        results.append(t_out)
    return results

@router.post("/", response_model=TeamOut)
def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.STAFF]:
        raise HTTPException(status_code=403, detail="Not authorized to create teams")
        
    db_team = Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.put("/{team_id}", response_model=TeamOut)
def update_team(
    team_id: int,
    team: TeamUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.STAFF]:
         raise HTTPException(status_code=403, detail="Not authorized")

    db_team = db.query(Team).filter(Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
        
    for key, value in team.dict().items():
        setattr(db_team, key, value)
        
    db.commit()
    db.refresh(db_team)
    return db_team
