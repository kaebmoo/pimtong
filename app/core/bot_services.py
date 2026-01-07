from sqlalchemy.orm import Session
from app.models.models import User, Job, JobStatus, JobHistory, Assignment, Project
from app.core.security import verify_password, get_password_hash
from app.core.database import SessionLocal
from datetime import date, datetime, timedelta
from sqlalchemy import or_, and_, desc
from sqlalchemy.orm import joinedload

def get_db_session():
    return SessionLocal()

class BotService:
    @staticmethod
    def verify_user_login(username, password):
        """Verify username/password and return User object if valid."""
        db = get_db_session()
        try:
            user = db.query(User).filter(User.username == username).first()
            if not user:
                return None
            if not verify_password(password, user.password_hash):
                return None
            return user
        finally:
            db.close()

    @staticmethod
    def link_telegram_id(username, telegram_id):
        """Update user's telegram_id."""
        db = get_db_session()
        try:
            user = db.query(User).filter(User.username == username).first()
            if user:
                user.telegram_id = str(telegram_id)
                db.add(user)
                db.commit()
                db.refresh(user)
                return True
            return False
        finally:
            db.close()

    @staticmethod
    def get_user_by_telegram_id(telegram_id):
        """Get user by telegram_id."""
        db = get_db_session()
        try:
            return db.query(User).filter(User.telegram_id == str(telegram_id)).first()
        finally:
            db.close()

    @staticmethod
    def update_password(user_id, new_password):
        """Update user password."""
        db = get_db_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.password_hash = get_password_hash(new_password)
                db.add(user)
                db.commit()
                return True
            return False
        finally:
            db.close()

    @staticmethod
    def get_jobs(user_id, filters=None):
        """
        Get jobs based on filters and user role.
        """
        db = get_db_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return []

            query = db.query(Job)

            # --- Permission & Technician Filter Logic ---
            tech_name = filters.get('technician_name') if filters else None
            
            if user.role in ['admin', 'manager']:
                # Admin can see all. Check if filtering by specific tech.
                if tech_name:
                    # Find technician by name (partial match)
                    tech = db.query(User).filter(User.full_name.ilike(f"%{tech_name}%") | User.username.ilike(f"%{tech_name}%")).first()
                    if tech:
                        query = query.join(Assignment).filter(Assignment.technician_id == tech.id)
                    else:
                        return [] # Tech not found
                else:
                    # No specific tech asked, show ALL jobs (or unassigned too?)
                    # If query is "My jobs", show admin's jobs? Usually admins want to see overview.
                    # Let's default to ALL jobs if no tech specified for Admin.
                    pass 
            else:
                # Regular staff/technician -> Only own jobs
                query = query.join(Assignment).filter(Assignment.technician_id == user.id)

            if filters:
                # Date Filter
                today = date.today()
                target_date = filters.get('date')
                period = filters.get('period')

                if target_date == 'today':
                    query = query.filter(Job.scheduled_date == today)
                elif target_date == 'tomorrow':
                    query = query.filter(Job.scheduled_date == today + timedelta(days=1))
                elif target_date == 'yesterday':
                    query = query.filter(Job.scheduled_date == today - timedelta(days=1))
                elif target_date:
                     # Try to parse YYYY-MM-DD
                     try:
                         query = query.filter(Job.scheduled_date == datetime.strptime(target_date, "%Y-%m-%d").date())
                     except:
                         pass
                
                if period == 'week':
                    start_week = today - timedelta(days=today.weekday())
                    end_week = start_week + timedelta(days=6)
                    query = query.filter(Job.scheduled_date.between(start_week, end_week))
                elif period == 'next_week':
                    start_next = today + timedelta(days=(7 - today.weekday()))
                    end_next = start_next + timedelta(days=6)
                    query = query.filter(Job.scheduled_date.between(start_next, end_next))
                elif period == 'last_week':
                    # Monday of this week
                    this_monday = today - timedelta(days=today.weekday())
                    start_last = this_monday - timedelta(days=7)
                    end_last = start_last + timedelta(days=6)
                    query = query.filter(Job.scheduled_date.between(start_last, end_last))

                # Status Filter
                status = filters.get('status')
                if status:
                    if status == 'active': # Pending or In Progress
                        query = query.filter(Job.status.in_([JobStatus.PENDING, JobStatus.IN_PROGRESS, JobStatus.ASSIGNED]))
                    elif status == 'completed':
                        query = query.filter(Job.status == JobStatus.COMPLETED)
                    # Add more matches as needed

                # Customer Filter
                customer_name = filters.get('customer_name')
                if customer_name:
                    query = query.filter(Job.customer_name.ilike(f"%{customer_name}%"))

                # Keyword Filter
                keyword = filters.get('keyword')
                if keyword:
                    query = query.filter(
                        or_(
                            Job.title.ilike(f"%{keyword}%"),
                            Job.description.ilike(f"%{keyword}%"),
                            Job.product_type.ilike(f"%{keyword}%"),
                            Job.model.ilike(f"%{keyword}%")
                        )
                    )

            # Order by date
            query = query.order_by(Job.scheduled_date.asc(), Job.scheduled_time.asc())
            
            # Eager load assignments and technicians to prevent DetachedInstanceError
            # when accessing job.assignments in the bot (after session closed)
            query = query.options(
                joinedload(Job.assignments).joinedload(Assignment.technician)
            )
            
            return query.all()
        finally:
            db.close()

    @staticmethod
    def get_projects(filters=None):
        """
        Get projects based on filters.
        """
        db = get_db_session()
        try:
            query = db.query(Project)
            
            if filters:
                keyword = filters.get('keyword')
                if keyword:
                    query = query.filter(Project.name.ilike(f"%{keyword}%"))
                
                status = filters.get('status')
                if status:
                     query = query.filter(Project.status == status)

            return query.all()
        finally:
            db.close()

    @staticmethod
    def get_project_details(project_id=None, project_name=None):
        """Get detailed project info including job stats."""
        db = get_db_session()
        try:
            query = db.query(Project)
            if project_id:
                project = query.filter(Project.id == project_id).first()
            elif project_name:
                project = query.filter(Project.name.ilike(f"%{project_name}%")).first()
            else:
                return None

            if not project:
                return None

            # Calculate stats
            total_jobs = len(project.jobs)
            completed_jobs = sum(1 for j in project.jobs if j.status == JobStatus.COMPLETED)
            progress = int((completed_jobs / total_jobs * 100) if total_jobs > 0 else 0)
            
            # Format dates
            start_date = project.start_date.strftime("%d/%m/%Y") if project.start_date else "-"
            end_date = project.end_date.strftime("%d/%m/%Y") if project.end_date else "-"

            # Collect Job Titles
            job_list = [f"{j.title} ({j.status})" for j in project.jobs]

            return {
                "id": project.id,
                "name": project.name,
                "customer": project.customer_name,
                "description": project.description,
                "status": project.status,
                "progress": progress,
                "total_jobs": total_jobs,
                "start_date": start_date,
                "end_date": end_date,
                "job_list": job_list
            }
        finally:
            db.close()

    @staticmethod
    def get_job_details(job_id, user_id):
        """Get full details of a specific job (Security Check included)."""
        db = get_db_session()
        try:
            # Check assignment first
            query = db.query(Job).join(Assignment).filter(
                Assignment.technician_id == user_id,
                Job.id == job_id
            ).options(
                joinedload(Job.assignments).joinedload(Assignment.technician)
            )
            job = query.first()
            return job
        finally:
            db.close()

    @staticmethod
    def update_job_status(job_id, user_id, new_status, note=None):
        """Update job status and add log."""
        db = get_db_session()
        try:
            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                return False, "Job not found"

            # Check permissions (simple check via assignments)
            is_assigned = db.query(Assignment).filter(
                Assignment.job_id == job_id, 
                Assignment.technician_id == user_id
            ).first()
            
            if not is_assigned:
                return False, "Not authorized"

            old_status = job.status
            job.status = new_status
            
            # Add History
            history = JobHistory(
                job_id=job.id,
                user_id=user_id,
                old_status=old_status,
                new_status=new_status,
                note=note or f"Updated via Telegram Bot"
            )
            db.add(history)
            db.commit()
            return True, "Updated successfully"
        finally:
            db.close()
