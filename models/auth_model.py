from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class UserActivation(Base):
    __tablename__ = "user_activations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String(36), nullable=False, unique=True)  # UUID token
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", backref="activation_links")
