from motor.motor_asyncio import AsyncIOMotorClient
from asyncio import get_event_loop
from json import loads
from os import getenv
from bson import ObjectId, json_util
from pymongo import MongoClient
from db import cache


def dump_query(q):
    return json_util.dumps(q).replace('"', "'")


def load_query(q):
    return loads(q.replace("'", '"').replace("$oid", "objectId"))


class Mongo:
    connection = []

    def __init__(self, credentials, queries=[]):
        self.uri_name = credentials['uri'] if credentials['secure'] else credentials['uri']
        self.pipelines = queries
        val = next((item for item in self.connection if item["uri"] == self.uri_name),
                   False) if self.connection else False
        if not val:
            self.save_connection(self.uri_name, credentials['name'])
        else:
            print("Connection Saved Already")
        self.get_result_and_cache(self.pipelines)

    def save_connection(self, uri_name, table):
        print("In Save Connection")
        uri = getenv(uri_name)
        client = AsyncIOMotorClient(uri)
        db = client[table]
        dic = {'uri': uri_name, 'client': client, 'db': db}
        self.connection.append(dic)

    @cache
    def get_result_and_cache(self, pipeline):
        loop = get_event_loop()
        query_results = loop.run_until_complete(self.fetch_results(pipeline))
        return query_results

    async def fetch_results(self, pipeline):
        list_element = []
        val = next((item for item in self.connection if item["uri"] == self.uri_name),False)
        if not val:
            for pip in pipeline:
                collection = val['db'][pip["table"]]
                async for doc in collection.aggregate(load_query(pip["input"])):
                    list_element.append(doc)
        return list_element
