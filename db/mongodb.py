from motor.motor_asyncio import AsyncIOMotorClient
from asyncio import get_event_loop
from json import loads
from os import getenv
from bson import ObjectId, json_util
from db import cache


def dump_query(q):
    return json_util.dumps(q).replace('"', "'")


def load_query(q):
    return loads(q.replace("'", '"').replace("$oid", "objectId"))


class Mongo:

    def __init__(self, credentials, queries=[]):
        self.URI = getenv(credentials['uri']) if credentials['secure'] else eval(
            credentials['uri'])
        self.client = AsyncIOMotorClient(self.URI)
        self.db = self.client[credentials['name']]
        self.pipelines = queries

    @cache
    def get_result_and_cache(self):
        loop = get_event_loop()
        query_results = loop.run_until_complete(self.fetch_results())
        return query_results

    async def fetch_results(self):
        query_results = []
        for pipeline in self.pipelines:
            list_element = []
            print(pipeline)
            async for doc in self.db[pipeline["table"]].aggregate(load_query(pipeline["input"])):
                list_element.append(doc)
            query_results.append(list_element)
        return query_results
