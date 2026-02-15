from decimal import Decimal, ROUND_HALF_UP
from pydantic import Field, field_validator, field_serializer

from db import db

from models.TypedCollection import TypedCollection
from models.MongoModelBase import MongoModelBase


class Product(MongoModelBase):
    name: str = Field(...)
    cost: Decimal = Field(..., gt=Decimal(0), decimal_places=2)
    stock: int = Field(default=0, ge=0)

    @field_validator("cost", mode="after")
    @classmethod
    def force_two_decimals(cls, v: Decimal) -> Decimal:
        """Validation for the cost attribute, forces the value to always be represented with two decimal digits"""
        return v.quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

    @field_serializer("cost")
    def serialize_cost(self, cost: Decimal):
        """Forces the serialized format to have exactly two decimal digits"""
        return f"{cost:.2f}"


product_collection: TypedCollection[Product] = TypedCollection(db.product, Product)
