import asyncio

from models import user_collection
from models.user import User
from faker import Faker

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker()


async def main():
    for i in range(10):
        try:
            user_1 = User.model_validate(
                {"firstName": fake.first_name(), "lastName": fake.last_name()}
            )
            user_2 = User.model_validate(
                {"first_name": fake.first_name(), "last_name": fake.last_name()}
            )
            result_1 = await user_collection.insert_one(user_1)
            result_2 = await user_collection.insert_one(user_2)
            logger.info(f"{i:_<2}. added {result_1} and {result_2} to MongoDB.")
        except ValueError as e:
            logger.error(e)

    try:
        print(await user_collection.find({"first_name": {"$regex": "an"}}))
        print(await user_collection.count_documents())
    except ValueError as e:
        logger.error(e)


if __name__ == "__main__":
    asyncio.run(main())
