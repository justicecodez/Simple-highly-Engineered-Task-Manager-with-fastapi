from app.model.model import Base

from sqlalchemy import Column, Integer, String, DateTime, Boolean

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    title = Column(String(255))
    description = Column(String(255))
    status = Column(String(50), default="pending")
    priority= Column(String(50), default="medium")
    due_date = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False)
    