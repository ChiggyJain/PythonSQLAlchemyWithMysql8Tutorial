
from app.database.db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=False, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # parent -> child relationship established
    posts = relationship("Post", back_populates="user", cascade="all,delete,delete-orphan")
    # means ONE profile per user
    profile = relationship("Profile", back_populates="user", uselist=False)
    
