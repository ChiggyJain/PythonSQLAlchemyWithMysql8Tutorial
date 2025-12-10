
from app.database.db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    # adding foreign key relationship from User model
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # child -> parent relationship established in User model
    user = relationship("User", back_populates="posts")