from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_serializer, model_validator
from typing import Any


class MongoModelBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    id: ObjectId = Field(alias="_id", default_factory=ObjectId)

    @field_serializer("id")
    def serialize_objectid(self, id_: ObjectId) -> str:
        """Serialize ObjectId to string."""
        return str(id_)

    @model_validator(mode="before")  # noqa
    @classmethod
    def validate_objectid(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Convert string ObjectId to ObjectId objects."""
        if isinstance(data, dict) and "_id" in data and isinstance(data["_id"], str):
            data["_id"] = ObjectId(data["_id"])
        return data

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        attrs = []
        for field_name, field in self.model_fields.items():
            value = getattr(self, field_name)
            if field_name == "id" and isinstance(value, ObjectId):
                attrs.append(f"id='{str(value)}'")
            else:
                attrs.append(f"{field_name}={repr(value)}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"
