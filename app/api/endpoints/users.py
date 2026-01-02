from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import User, UserRole
from pydantic import BaseModel
from app.core.security import get_password_hash
from app.api.deps import get_current_user

router = APIRouter()

class UserBase(BaseModel):
    username: str
    full_name: str
    role: UserRole
    phone_number: str
    email: Optional[str] = None
    telegram_id: Optional[str] = None
    team_id: Optional[int] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    telegram_id: Optional[str] = None
    team_id: Optional[int] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username, 
        password_hash=hashed_password, 
        full_name=user.full_name, 
        role=user.role,
        phone_number=user.phone_number,
        email=user.email,
        telegram_id=user.telegram_id,
        team_id=user.team_id,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserOut)
def read_user_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.put("/me", response_model=UserOut)
def update_user_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    update_data = user_update.dict(exclude_unset=True)
    
    if 'password' in update_data:
        password = update_data.pop('password')
        current_user.password_hash = get_password_hash(password)
        
    for key, value in update_data.items():
        setattr(current_user, key, value)
        
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # PERMISSION CHECK (Mockup Logic)
    # Logic: Only self or Admin can edit.
    # checking logic would ideally use current_user.
    pass
    
    update_data = user_update.dict(exclude_unset=True)
    if 'password' in update_data:
        password = update_data.pop('password')
        db_user.password_hash = get_password_hash(password)
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Soft delete prefered usually, but for now strict delete or toggle active
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # PERMISSION CHECK: Admin only
    # Real app: if current_user.role != UserRole.ADMIN: raise 403
    
    db.delete(db_user)
    db.commit()
    return None
