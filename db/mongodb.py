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
        self.uri_name = getenv(credentials['uri']) if credentials['secure'] else credentials['uri']
        self.pipelines = queries
        val = next((item for item in self.connection if item["uri"] == self.uri_name),
                   False) if self.connection else False
        if not val:
            self.get_and_save_connection(self.uri_name, credentials['name'])
        else:
            print("Connection Saved Already")

    def get_and_save_connection(self, uri, table):
        print("In Save Connection")
        client = AsyncIOMotorClient(uri)
        db = client[table]
        dic = {'uri': uri, 'client': client, 'db': db}
        self.connection.append(dic)

    @cache
    def get_result_and_cache(self):
        loop = get_event_loop()
        query_results = loop.run_until_complete(self.fetch_results(self.pipelines))
        return query_results

    async def fetch_results(self, pipeline):
        list_element = []
        val = next((item for item in self.connection if item["uri"] == self.uri_name),False)
        if val:
            for pip in pipeline:
                print(pip)
                collection = val['db'][pip["source"]]
                print(collection)
                d = []
                async for doc in collection.aggregate(load_query(pip["value"])):
                    print(doc)
                    d.append(doc)
                list_element.append(d if len(d) > 1 else d[0])
        return list_element
