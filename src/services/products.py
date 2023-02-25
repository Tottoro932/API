from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime

from src.db.db import get_session
from src.models.products import Products
from src.models.schemas.products.products_request import ProductRequest


class ProductsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Products]:
        products = (
            self.session
                .query(Products)
                .order_by(
                Products.id.desc()
            )
                .all()
        )
        return products

    def get(self, product_id: int) -> Products:
        product = (
            self.session
                .query(Products)
                .filter(
                Products.id == product_id
            )
                .first()
        )
        return product

    def add(self, product_schema: ProductRequest, created_user_id: int) -> Products:
        datetime_ = datetime.utcnow()
        product = Products(
            **product_schema.dict(),
            created_at=datetime_,
            created_by=created_user_id,
            modifed_at=datetime_,
            modifed_by=created_user_id
        )
        self.session.add(product)
        self.session.commit()
        return product

    def update(self, product_id: int, product_schema: ProductRequest, modifed_user_id: int) -> Products:
        product = self.get(product_id)
        for field, value in product_schema:
            setattr(product, field, value)
        datetime_ = datetime.utcnow()
        setattr(product, 'modifed_at', datetime_)
        setattr(product, 'modifed_by', modifed_user_id)
        self.session.commit()
        return product

    def delete(self, product_id: int):
        product = self.get(product_id)
        self.session.delete(product)
        self.session.commit()
