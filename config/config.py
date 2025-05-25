import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
if CONNECTION_STRING is None:
    raise ValueError("Error loading CONNECTION_STRING environmental variable")


class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str


settings = Settings(MONGO_CONNECTION_STRING=CONNECTION_STRING)
