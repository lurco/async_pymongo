from pymongo import AsyncMongoClient

from config import settings

client: AsyncMongoClient[dict] = AsyncMongoClient(settings.MONGO_CONNECTION_STRING)

db = client.my_database
