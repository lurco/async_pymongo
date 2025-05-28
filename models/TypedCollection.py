from typing import Any, Generic, TypeVar

from pydantic import PositiveInt
from pymongo.asynchronous.collection import AsyncCollection
from models.MongoModelBase import MongoModelBase, MongoMixinWithId

T = TypeVar("T", bound=MongoModelBase)


class TypedCollection(Generic[T]):
    """A wrapper around AsyncCollection that provides automatic Pydantic model conversion"""

    @staticmethod
    def mongo_model_factory(model_base: type[T]) -> type[T | MongoMixinWithId]:
        class MongoModel(model_base, MongoMixinWithId):  # type: ignore
            pass

        return MongoModel

    def __init__(
        self,
        collection: AsyncCollection[dict[str, Any]],
        model_base: type[T],
    ):
        self._collection = collection
        self._model_base = model_base
        self._model = self.__class__.mongo_model_factory(self._model_base)

    async def insert_one(self, model_instance: T) -> T | MongoMixinWithId:
        """Insert a Pydantic model instance"""
        doc = model_instance.model_dump(by_alias=True)
        result = await self._collection.insert_one(doc)
        inserted_doc = await self._collection.find_one({"_id": result.inserted_id})
        return self._model.model_validate(inserted_doc)

    async def find_one(self, filter_: dict[str, Any]) -> T | MongoMixinWithId | None:
        """Find one document and return as Pydantic model"""
        doc = await self._collection.find_one(filter_)
        if doc:
            return self._model.model_validate(doc)
        return None

    async def find(
        self,
        filter_: dict[str, Any] | None = None,
        skip: int = 0,
        limit: int | None = None,
        sort: list[tuple[str, int]] | None = None,
    ) -> tuple[T | MongoMixinWithId, ...]:
        """Find multiple documents with pagination and sorting and return as Pydantic models"""

        cursor = self._collection.find(filter_ or {})

        if sort:
            cursor = cursor.sort(sort)
        if skip > 0:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)

        docs = await cursor.to_list(length=limit)

        return tuple(self._model.model_validate(doc) for doc in docs)

    async def update_one(
        self, filter_: dict[str, Any], update: dict[str, Any]
    ) -> T | MongoMixinWithId | None:
        """Update one document"""
        result = await self._collection.update_one(filter_, update)
        if result.modified_count > 0:
            updated_doc = await self._collection.find_one(filter_)
            return self._model.model_validate(updated_doc) if updated_doc else None
        return None

    async def delete_one(self, filter_: dict[str, Any]) -> bool:
        """Delete one document"""
        result = await self._collection.delete_one(filter_)
        return result.deleted_count > 0

    async def count_documents(
        self, filter_: dict[str, Any] | None = None
    ) -> PositiveInt:
        """Count documents matching filter"""
        return await self._collection.count_documents(filter_ or {})

    def __repr__(self) -> str:
        """Return a string representation of the collection."""
        return f"{self.__class__.__name__}(collection={self._collection.name}, model={self._model_base.__name__})"
