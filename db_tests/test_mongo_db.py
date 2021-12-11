import random
import time

from pymongo import MongoClient
from pymongo.database import Database

mongo_url: str = "mongodb://localhost:27017"
client: MongoClient = MongoClient(mongo_url)
test_db: Database = client.test_db


def saving_data_test():
    start = time.time()
    for i in range(10000):
        test_db.test_data.insert_one({"id": i, "some_data": f"some_data_{i}"})
    return time.time() - start


def get_data_test():
    start = time.time()
    data = test_db.test_data.find()
    for _ in data:
        continue
    return time.time() - start


def find_data_test():
    start = time.time()
    random_id = random.randint(0, 10000)
    data = test_db.test_data.find({}, {"id": random_id})
    for _ in data:
        continue
    return time.time() - start


if __name__ == '__main__':
    print(saving_data_test())
    print(get_data_test())
    print(find_data_test())
