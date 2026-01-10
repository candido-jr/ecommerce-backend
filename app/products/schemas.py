from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductFilter(BaseModel):
    # product-level filters
    q: str | None = Field(default=None, min_length=1, description="search query")
    name: str | None = Field(default=None, min_length=1)

    # sorting
    sort: str | None = Field(default=None)
    order: str = Field(default="desc", description="asc|desc")
