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
    technician: TechnicianOut
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Job)
    
    # RBAC Filtering
    if current_user.role == UserRole.TECHNICIAN:
        query = query.join(Assignment).filter(
            or_(
                Assignment.technician_id == current_user.id,
                Assignment.team_id == current_user.team_id
            )
        ).distinct()
        
    if project_id:
        query = query.filter(Job.project_id == project_id)
        
    jobs = query.offset(skip).limit(limit).all()
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
    if current_user.role == UserRole.TECHNICIAN:
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
    
    # RBAC: Technicians can only update status (and maybe notes in future), but for now we trust the UI hiding
    # Ideally should filter update_data here if Tech
    
    update_data = job_update.dict(exclude_unset=True)
    
    # Update fields first (so we respect manual status changes unless it's just defaulting to pending)
    assignments_to_process = None
    if 'technician_ids' in update_data:
        assignments_to_process = update_data.pop('technician_ids')
        
    for key, value in update_data.items():
        setattr(db_job, key, value)
        
    # Handle assignments update
    if assignments_to_process is not None:
        # RBAC: Technicians cannot re-assign logic
        if current_user.role == UserRole.TECHNICIAN:
             # Skip assignment processing for techs effectively
             pass
        else:
            technician_ids = assignments_to_process
            # Simple strategy: remove all and re-add (for now)
            db.query(Assignment).filter(Assignment.job_id == job_id).delete()
            
            if technician_ids:
                # Auto-update status workflow
                # Only if status is currently PENDING (either from DB or just updated from form as PENDING)
                if db_job.status == JobStatus.PENDING:
                    db_job.status = JobStatus.ASSIGNED
                    # No need to add() again, existing session references object
    
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
