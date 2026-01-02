from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, ForeignKey, DateTime, inspect
from sqlalchemy.sql import func
import sys
import os

# Put app in path
sys.path.append(os.getcwd())

from app.core.database import SQLALCHEMY_DATABASE_URL

def migrate():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    metadata = MetaData()
    inspector = inspect(engine)

    # 1. Add location columns to 'jobs' table
    with engine.connect() as conn:
        columns = [col['name'] for col in inspector.get_columns('jobs')]
        
        if 'location_lat' not in columns:
            print("Adding location_lat to jobs...")
            conn.execute("ALTER TABLE jobs ADD COLUMN location_lat VARCHAR")
        
        if 'location_long' not in columns:
            print("Adding location_long to jobs...")
            conn.execute("ALTER TABLE jobs ADD COLUMN location_long VARCHAR")

    # 2. Create 'assignments' table if not exists
    if not inspector.has_table('assignments'):
        print("Creating assignments table...")
        assignments = Table(
            'assignments', metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('job_id', Integer, ForeignKey('jobs.id')),
            Column('technician_id', Integer, ForeignKey('users.id')),
            Column('assigned_at', DateTime(timezone=True), server_default=func.now()),
            Column('check_in_time', DateTime(timezone=True), nullable=True),
            Column('check_out_time', DateTime(timezone=True), nullable=True),
            Column('completion_notes', Text, nullable=True),
            Column('rating', Integer, nullable=True)
        )
        metadata.create_all(engine)
    
    print("Migration V2 completed successfully.")

if __name__ == "__main__":
    migrate()
