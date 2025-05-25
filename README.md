# PyMongo Test

---

A simple demonstration project showing how to use PyMongo with Pydantic for type-safe MongoDB interactions in Python.

## Overview

This project demonstrates:
- Using PyMongo's asynchronous client for MongoDB operations
- Implementing Pydantic models for data validation and type safety
- Creating a typed collection wrapper for automatic model conversion
- Handling MongoDB ObjectId with Pydantic
- Using field aliases to support different naming conventions

## Requirements

- Python 3.13+
- MongoDB server

## Installation

1. Clone the repository
2. Install dependencies with uv

```
uv sync
```

> You can also use pip (`pip install -e .`) or poetry (`poetry install`) etc.

3. Create a `.env` file with your MongoDB connection string:

```
CONNECTION_STRING=mongodb://localhost:27017
```

## Usage

Run the example:

```sh
uv run main.py
```

Or activate the virtual environment and then you can:
```shell
python main.py
```

### Creating and storing models

```python
# Create a user with Pydantic validation
user = User.model_validate({"firstName": "John", "lastName": "Doe"}) # first_name and last_name work too because we use populate_by_name=True

# Insert into MongoDB (id is created automatically on the Python side)
await user_collection.insert_one(user)

# Query users with MongoDB filters
# Find all users
all_users = await user_collection.find({})

# Find users by exact match
john_users = await user_collection.find({"firstName": "John"})

# Find users with comparison operators
users_not_john = await user_collection.find({"firstName": {"$ne": "John"}})

# Find users with logical operators
users_john_or_jane = await user_collection.find({"$or": [
    {"firstName": "John"}, 
    {"firstName": "Jane"}
]})

# Find users with regex pattern
users_j_names = await user_collection.find({"firstName": {"$regex": "^J"}})

# Count documents with filter
count = await user_collection.count_documents({"lastName": "Doe"})
```

## Project Structure

- `models/` - Pydantic models and MongoDB collection wrappers
  - `MongoModelBase.py` - Base class for MongoDB models with ObjectId support
  - `TypedCollection.py` - Generic wrapper for MongoDB collections with Pydantic conversion
  - `user.py` - Example User model implementation
- `db/` - Database connection setup
- `config/` - Configuration using environment variables and Pydantic settings

## Key Components

### TypedCollection

A generic wrapper around PyMongo's `AsyncCollection` that provides automatic conversion between MongoDB documents and Pydantic models:

```python
# Create a typed collection
user_collection: TypedCollection[User] = TypedCollection(db.user, User)

# Use it with automatic model conversion
await user_collection.insert_one(user)  # Converts model to dict
```

### MongoModelBase

Base class for MongoDB models with proper ObjectId handling:

```python
class MongoModelBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    id_: ObjectId = Field(alias="id", default_factory=ObjectId)
```

## Configuration

The project uses environment variables for configuration:
- `CONNECTION_STRING` - MongoDB connection string

Load from `.env` file or set in your environment.
