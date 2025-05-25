from pydantic import Field, ConfigDict

from db import db
from models.MongoModelBase import MongoModelBase
from models.TypedCollection import TypedCollection


class User(MongoModelBase):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")


user_collection: TypedCollection[User] = TypedCollection(db.user, User)
