import time
import random

from elasticsearch import Elasticsearch

es_client: Elasticsearch = Elasticsearch("localhost:9200")


def saving_data_test():
    start = time.time()
    for i in range(10000):
        es_client.index(index="test_index", id=str(i), document={"id": i, "some_data": f"some_data_{i}"})
    return time.time() - start


def get_data():
    start = time.time()
    es_client.search(index="test_index", body={"query": {"match_all": {}}}, size=10000)
    return time.time() - start


def get_find_data():
    start = time.time()
    random_id = random.randint(0, 10000)
    es_client.search(index="test_index", body={"query": {"match": {"message": {"query": random_id}}}}, size=10000)
    return time.time() - start


if __name__ == '__main__':
    print(saving_data_test())
    print(get_data())
    print(get_find_data())
