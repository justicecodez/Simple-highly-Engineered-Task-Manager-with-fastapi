from app.model.model import Base
from sqlalchemy import Column, Integer, String,DateTime

class User(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True)
    name=Column(String(255))
    email=Column(String(255), unique=True)
    username=Column(String(255), unique=True)
    password=Column(String(255))
    created_at=Column(DateTime)
