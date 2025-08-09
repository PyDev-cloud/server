from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone=Column(String, nullable=False)
    alternative_Phone=Column(String, nullable=True)
    email=Column(String,nullable=False)
    role = Column(String, default="general")  # general, president, finance, expense, member