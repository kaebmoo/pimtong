from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Job, JobType, JobStatus, User, Assignment
from pydantic import BaseModel
from datetime import date
from typing import Optional, List

router = APIRouter()

class TechnicianOut(BaseModel):
    id: int
    full_name: str
    username: str # useful for avatar/display
    class Config:
        from_attributes = True

class JobBase(BaseModel):
    title: str
    description: Optional[str] = None
    job_type: JobType
    status: JobStatus = JobStatus.PENDING
    customer_name: str
    customer_phone: str
    customer_address: str
    location_lat: Optional[str] = None
    location_long: Optional[str] = None
    scheduled_date: date
    scheduled_time: Optional[str] = None
    project_id: Optional[int] = None

class JobCreate(JobBase):
    technician_ids: Optional[List[int]] = []

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    job_type: Optional[JobType] = None
    status: Optional[JobStatus] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    location_lat: Optional[str] = None
    location_long: Optional[str] = None
    scheduled_date: Optional[date] = None
    scheduled_time: Optional[str] = None
    project_id: Optional[int] = None
    technician_ids: Optional[List[int]] = None

class JobOut(JobBase):
    id: int
    assignments: List["AssignmentOut"] = []
    
    class Config:
        from_attributes = True

class AssignmentOut(BaseModel):
    technician: Optional[TechnicianOut] = None
    class Config:
        from_attributes = True
        
JobOut.update_forward_refs()

from app.api.deps import get_current_user
from app.models.models import UserRole

@router.post("/", response_model=JobOut)
def create_job(
    job: JobCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == UserRole.TECHNICIAN:
        raise HTTPException(status_code=403, detail="Technicians cannot create jobs")

    job_data = job.dict()
    technician_ids = job_data.pop('technician_ids', [])
    
    db_job = Job(**job_data)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    # Process assignments
    if technician_ids:
        # Auto-update status workflow
        if db_job.status == JobStatus.PENDING:
           db_job.status = JobStatus.ASSIGNED
           db.add(db_job)

        for tech_id in technician_ids:
            assignment = Assignment(job_id=db_job.id, technician_id=tech_id)
            db.add(assignment)
        db.commit()
        db.refresh(db_job)
        
    return db_job

from sqlalchemy import or_

@router.get("/", response_model=List[JobOut])
def read_jobs(
    skip: int = 0, 
    limit: int = 100, 
    project_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # DEBUG LOGS
    print(f"DEBUG: Read Jobs - User: {current_user.username}, Role: {current_user.role}, Search: {search}, Project: {project_id}")

    query = db.query(Job)
    
    # RBAC Filtering
    # Robust check for role type (Enum vs String)
    user_role_str = str(current_user.role.value if hasattr(current_user.role, 'value') else current_user.role).lower()
    
    if user_role_str == "technician":
        query = query.join(Assignment).filter(
            or_(
                Assignment.technician_id == current_user.id,
                Assignment.team_id == current_user.team_id if current_user.team_id else False
            )
        ).distinct()
        print(f"DEBUG: Applied Technician Filter for user {current_user.id}")
        
    if project_id:
        query = query.filter(Job.project_id == project_id)
        
    if search:
        search_term = f"%{search}%"
        # Check if search is strictly an integer for ID lookup
        id_match = None
        try:
            id_match = int(search)
        except ValueError:
            pass
            
        filters = [
            Job.title.ilike(search_term),
            Job.customer_name.ilike(search_term),
            Job.description.ilike(search_term)
        ]
        if id_match is not None:
            filters.append(Job.id == id_match)
            
        query = query.filter(or_(*filters))
        
    # Apply Sort
    query = query.order_by(Job.id.desc())
    
    jobs = query.offset(skip).limit(limit).all()
    print(f"DEBUG: Returning {len(jobs)} jobs")
    return jobs

@router.get("/{job_id}", response_model=JobOut)
def read_job(
    job_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
        
    # RBAC Check for single job view
    user_role_str = str(current_user.role.value if hasattr(current_user.role, 'value') else current_user.role).lower()
    
    if user_role_str == "technician":
        # Check if assigned directly or via team
        is_assigned = any(
            a.technician_id == current_user.id or 
            (current_user.team_id and a.team_id == current_user.team_id) 
            for a in job.assignments
        )
        if not is_assigned:
             raise HTTPException(status_code=403, detail="Not authorized to view this job")

    return job

@router.put("/{job_id}", response_model=JobOut)
def update_job(
    job_id: int, 
    job_update: JobUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # RBAC Security: Technicians can only edit their own jobs
    user_role_str = str(current_user.role.value if hasattr(current_user.role, 'value') else current_user.role).lower()
    
    if user_role_str == "technician":
         # Verify assignment
         is_assigned = db.query(Assignment).filter(
            Assignment.job_id == job_id,
            or_(
                Assignment.technician_id == current_user.id,
                Assignment.team_id == current_user.team_id if current_user.team_id else False
            )
         ).first()
         
         if not is_assigned:
             raise HTTPException(status_code=403, detail="You are not authorized to edit this job")
         
         # Prevent Techs from re-assigning
         if job_update.technician_ids is not None:
             raise HTTPException(status_code=403, detail="Technicians cannot change job assignments")
    
    update_data = job_update.dict(exclude_unset=True)
    
    # Update fields first (so we respect manual status changes unless it's just defaulting to pending)
    assignments_to_process = None
    if 'technician_ids' in update_data:
        assignments_to_process = update_data.pop('technician_ids')
        
    for key, value in update_data.items():
        setattr(db_job, key, value)
        
    # Handle assignments update
    if assignments_to_process is not None:
        if user_role_str == "technician":
             # Double check prevention (should be caught above)
             pass
        else:
            technician_ids = assignments_to_process
            # Simple strategy: remove all and re-add (for now)
            db.query(Assignment).filter(Assignment.job_id == job_id).delete()
            
            if technician_ids:
                if db_job.status == JobStatus.PENDING:
                    db_job.status = JobStatus.ASSIGNED
    
                for tech_id in technician_ids:
                    assignment = Assignment(job_id=job_id, technician_id=tech_id)
                    db.add(assignment)
        
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.delete("/{job_id}", status_code=204)
def delete_job(
    job_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Only Admins can delete jobs")

    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(db_job)
    db.commit()
    return None
