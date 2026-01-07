from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api import deps
from app.core.database import get_db
from app.models.models import Job, JobStatus, Project, User, UserRole, Assignment

router = APIRouter()

@router.get("/summary")
def get_summary_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Basic Stats
    total_jobs = db.query(Job).count()
    completed = db.query(Job).filter(Job.status == JobStatus.COMPLETED).count()
    pending = db.query(Job).filter(Job.status == JobStatus.PENDING).count()
    in_progress = db.query(Job).filter(Job.status == JobStatus.IN_PROGRESS).count()
    
    # Financials (Mock for now as we don't have revenue fields yet, or count sales)
    # total_revenue = ...
    
    return {
        "total_jobs": total_jobs,
        "completed": completed,
        "pending": pending,
        "in_progress": in_progress,
        "completion_rate": int((completed / total_jobs * 100) if total_jobs > 0 else 0)
    }

@router.get("/by_technician")
def get_jobs_by_technician(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.STAFF]:
         raise HTTPException(status_code=403, detail="Not authorized")

    # Group by technician
    # DB query to count assignments
    results = db.query(
        User.full_name, 
        func.count(Assignment.id).label('job_count')
    ).join(Assignment, User.id == Assignment.technician_id)\
     .group_by(User.id).all()
     
    data = [{"name": r[0], "count": r[1]} for r in results]
    return data

    return data

@router.get("/overdue")
def get_overdue_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    from datetime import datetime, date
    
    # Logic: Status NOT Completed/Cancelled AND (Date < Today OR (Date == Today and Time < Now))
    today = date.today()
    now_time = datetime.now().strftime("%H:%M")
    
    # 1. Past dates
    overdue_query = db.query(Job).filter(
        Job.status.notin_([JobStatus.COMPLETED, JobStatus.CANCELLED]),
        Job.scheduled_date < today
    )
    
    # 2. Today but past time (if time is set)
    # Using python filtering for time comparison to avoid complex SQL for string time
    today_jobs = db.query(Job).filter(
        Job.status.notin_([JobStatus.COMPLETED, JobStatus.CANCELLED]),
        Job.scheduled_date == today,
        Job.scheduled_time < now_time,
        Job.scheduled_time != None # explicit check
    ).all()
    
    results = overdue_query.all() + today_jobs
    
    # Format
    data = []
    for job in results:
        delta = (today - job.scheduled_date).days
        if delta == 0:
            duration = "Today"
        else:
            duration = f"{delta} days"
            
        data.append({
            "id": job.id,
            "title": job.title,
            "status": job.status,
            "scheduled_date": job.scheduled_date,
            "scheduled_time": job.scheduled_time,
            "technician": ", ".join([a.technician.full_name for a in job.assignments if a.technician]) if job.assignments else "Unassigned",
            "overdue_duration": duration
        })
        
    return data

@router.get("/export")
def export_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Return flat list for CSV export
    jobs = db.query(Job).all()
    data = []
    for job in jobs:
        data.append({
            "id": job.id,
            "title": job.title,
            "status": job.status,
            "customer": job.customer_name,
            "date": job.scheduled_date,
            "type": job.job_type,
            "project_id": job.project_id
        })
    return data
