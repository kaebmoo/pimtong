from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from app.api import deps
from app.core.database import get_db
from app.models.models import Project, User, UserRole, Job
from pydantic import BaseModel

router = APIRouter()

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    customer_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str = "active" # active, completed, on_hold

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    job_count: int = 0
    completion_percentage: int = 0
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[ProjectOut])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    projects = db.query(Project).offset(skip).limit(limit).all()
    results = []
    
    for p in projects:
        p_out = ProjectOut.from_orm(p)
        jobs = p.jobs
        total_jobs = len(jobs)
        p_out.job_count = total_jobs
        
        if total_jobs > 0:
            completed_jobs = len([j for j in jobs if j.status == 'completed'])
            p_out.completion_percentage = int((completed_jobs / total_jobs) * 100)
        else:
            p_out.completion_percentage = 0
            
        results.append(p_out)
        
    return results

@router.post("/", response_model=ProjectOut)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.STAFF]:
        raise HTTPException(status_code=403, detail="Not authorized to create projects")
        
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/{project_id}", response_model=ProjectOut)
def read_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    p_out = ProjectOut.from_orm(project)
    jobs = project.jobs
    total_jobs = len(jobs)
    p_out.job_count = total_jobs
    if total_jobs > 0:
        completed = len([j for j in jobs if j.status == 'completed'])
        p_out.completion_percentage = int((completed / total_jobs) * 100)
        
    return p_out

@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.STAFF]:
         raise HTTPException(status_code=403, detail="Not authorized")

    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    for key, value in project.dict(exclude_unset=True).items():
        setattr(db_project, key, value)
        
    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only Admins can delete projects")
        
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    db.delete(db_project)
    db.commit()
    return None
