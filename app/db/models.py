from sqlalchemy import Column, Integer, String
from app.db.database import async_Base as Base

class AsyncUser(Base):
    __tablename__ = "async_users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)