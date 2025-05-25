from typing import Generic, TypeVar, Any

from pydantic import PositiveInt
from pymongo.asynchronous.collection import AsyncCollection
from models.MongoModelBase import MongoModelBase

T = TypeVar("T", bound=MongoModelBase)


class TypedCollection(Generic[T]):
    """A wrapper around AsyncCollection that provides automatic Pydantic model conversion"""

    def __init__(self, collection: AsyncCollection[dict[str, Any]], model: type[T]):
        self._collection = collection
        self._model = model

    async def insert_one(self, model_instance: T) -> None:
        """Insert a Pydantic model instance"""
        doc = model_instance.model_dump(by_alias=True)
        await self._collection.insert_one(doc)

    async def find_one(self, filter_: dict[str, Any]) -> T | None:
        """Find one document and return as Pydantic model"""
        doc = await self._collection.find_one(filter_)
        if doc:
            return self._model.model_validate(doc)
        return None

    async def find(self, filter_: dict[str, Any] | None = None) -> tuple[T, ...]:
        """Find multiple documents and return as Pydantic models"""
        docs = await self._collection.find(filter_ or {}).to_list()
        return tuple(self._model.model_validate(doc) for doc in docs)

    async def update_one(self, filter_: dict[str, Any], update: dict[str, Any]) -> None:
        """Update one document"""
        await self._collection.update_one(filter_, update)

    async def delete_one(self, filter_: dict[str, Any]) -> None:
        """Delete one document"""
        await self._collection.delete_one(filter_)

    async def count_documents(
        self, filter_: dict[str, Any] | None = None
    ) -> PositiveInt:
        """Count documents matching filter"""
        return await self._collection.count_documents(filter_ or {})

    def __repr__(self) -> str:
        """Return a string representation of the collection."""
        return f"{self.__class__.__name__}(collection={self._collection.name}, model={self._model.__name__})"
