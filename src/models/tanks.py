from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from src.models.base import Base


# from src.models.products import Products
# from src.models.users import Users


class Tanks(Base):
    __tablename__ = 'tanks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    max_capacity = Column(Float)
    current_capacity = Column(Float)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    created_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    modifed_at = Column(DateTime)
    modifed_by = Column(Integer, ForeignKey('users.id'), nullable=True)

    prod = relationship('Products', foreign_keys=[product_id], backref='product_tanks')
    user_cr = relationship('Users', foreign_keys=[created_by], backref='created_tanks')
    user_md = relationship('Users', foreign_keys=[modifed_by], backref='modifed_tanks')
