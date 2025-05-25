import asyncio

from models import user_collection
from models.user import User


async def main():
    try:
        user = User.model_validate({"firstName": "Jerzy", "lastName": "Coniewierzy"})
        await user_collection.insert_one(user)
        print(await user_collection.find())
        print(await user_collection.count_documents())
    except ValueError as e:
        print(e)

    try:
        user = User.model_validate(
            {"first_name": "Mateusz", "last_name": "Wajchęprzełóż"}
        )
        await user_collection.insert_one(user)
        print(await user_collection.find())
        print(await user_collection.count_documents())
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())
