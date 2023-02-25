from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.models.base import Base


class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    modifed_at = Column(DateTime)
    modifed_by = Column(Integer, ForeignKey('users.id'), nullable=True)

    user_cr = relationship('Users', foreign_keys=[created_by], backref='created_products')
    user_md = relationship('Users', foreign_keys=[modifed_by], backref='modifed_products')
