from sqlalchemy import Column, Integer, String, DateTime
from src.models.base import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password_hashed = Column(String, nullable=False)
    role = Column(String, default='viewer')
    created_at = Column(DateTime)
    created_by = Column(Integer, nullable=True)
    modifed_at = Column(DateTime)
    modifed_by = Column(Integer, nullable=True)
