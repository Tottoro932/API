from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from src.models.base import Base


class Operations(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True)
    mass = Column(Float)
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    tank_id = Column(Integer, ForeignKey('tanks.id'), nullable=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    created_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    modifed_at = Column(DateTime)
    modifed_by = Column(Integer, ForeignKey('users.id'), nullable=True)

    user_cr = relationship('Users', foreign_keys=[created_by], backref='created_operations')
    user_md = relationship('Users', foreign_keys=[modifed_by], backref='modifed_operations')
    prod = relationship('Products', foreign_keys=[product_id], backref='product_operation')
    tanks = relationship('Tanks', foreign_keys=[tank_id], backref='tanks_operations')
