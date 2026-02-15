import asyncio
import random
import sys
from decimal import Decimal

from config.logger import CustomFormatter
from models import user_collection
from models.product import product_collection, Product
from models.user import User
from faker import Faker

import logging

logging_handler = logging.StreamHandler(sys.stdout)
logging_handler.setFormatter(CustomFormatter())
logging.basicConfig(level=logging.INFO, handlers=[logging_handler])
logger = logging.getLogger(__name__)

fake = Faker()


async def create_users() -> None:
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


async def create_products() -> None:
    for i in range(50):
        try:
            product = Product.model_validate(
                {
                    "name": fake.word(),
                    "cost": Decimal((random.random() - 0.1) * 100000).quantize(
                        Decimal("0.01")
                    ),
                    "stock": random.randint(-3, 20000),
                }
            )
            result = await product_collection.insert_one(product)
            result_dict = result.model_dump(by_alias=True)
            logger.info(
                f"{i:_<2} Product {result_dict.get("name")} got added with price {result_dict.get("cost")} and stock amount {result_dict.get("stock")}."
            )
        except Exception as e:
            logger.error(e)


async def main():
    await create_users()
    await create_products()


if __name__ == "__main__":
    asyncio.run(main())
