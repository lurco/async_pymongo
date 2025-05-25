from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class MongoModelBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    id_: ObjectId = Field(alias="id", default_factory=ObjectId)
