from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.products.models import Product
from app.products.schemas import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())

        self.db.add(product)
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError("Integrity error while creating product") from e

        self.db.refresh(product)
        return product

    def get(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def list(self, *, skip: int = 0, limit: int = 50) -> list[Product]:
        stmt = select(Product).offset(skip).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    def update(self, product_id: int, data: ProductUpdate) -> Product | None:
        product = self.get(product_id)
        if product is None:
            return None

        updates = data.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(product, key, value)

        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError("Integrity error while updating product") from e

        self.db.refresh(product)
        return product

    def delete(self, product_id: int) -> bool:
        product = self.get(product_id)
        if product is None:
            return False

        self.db.delete(product)
        self.db.commit()
        return True
