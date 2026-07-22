from app.model.model import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class RefreshTokenRequest(Base):
    __tablename__ = "refresh_token_request"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    token_hash = Column(String(255))
    created_at = Column(DateTime)
    expires_at = Column(DateTime)
    revoked_at = Column(Boolean, default=False)
