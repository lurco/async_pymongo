import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB_NAME", "mydatabase")


class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str
    MONGO_DB_NAME: str

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        attrs = []
        for field_name in self.model_fields:
            value = getattr(self, field_name)
            attrs.append(f"{field_name}={repr(value)}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"


settings = Settings(MONGO_CONNECTION_STRING=CONNECTION_STRING, MONGO_DB_NAME=DB_NAME)
