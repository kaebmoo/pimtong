from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"
    TECHNICIAN = "technician"

class JobType(str, enum.Enum):
    SALES = "sales"
    PROJECT = "project"
    SERVICE = "service"

class JobStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    color = Column(String, default="#0ea5e9") # Hex color for UI
    
    members = relationship("User", back_populates="team")
    assignments = relationship("Assignment", back_populates="team")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    customer_name = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(String, default="active") # active, completed, on_hold
    
    jobs = relationship("Job", back_populates="project")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    full_name = Column(String)
    role = Column(String, default=UserRole.TECHNICIAN)
    
    # New Team Field
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    
    telegram_id = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    team = relationship("Team", back_populates="members")
    assignments = relationship("Assignment", back_populates="technician")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    job_type = Column(String, default=JobType.SERVICE)
    status = Column(String, default=JobStatus.PENDING)
    
    # Optional Project Link
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    customer_name = Column(String)
    customer_phone = Column(String)
    customer_address = Column(Text)
    location_lat = Column(String, nullable=True)
    location_long = Column(String, nullable=True)
    
    scheduled_date = Column(Date)
    scheduled_time = Column(String, nullable=True) # e.g. "14:00" or "Morning"
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project", back_populates="jobs")
    assignments = relationship("Assignment", back_populates="job")

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    
    # Polymorphic-like assignment: Either Tech OR Team
    technician_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Performance tracking
    check_in_time = Column(DateTime(timezone=True), nullable=True)
    check_out_time = Column(DateTime(timezone=True), nullable=True)
    completion_notes = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True) # 1-5

    job = relationship("Job", back_populates="assignments")
    technician = relationship("User", back_populates="assignments")
    team = relationship("Team", back_populates="assignments")

