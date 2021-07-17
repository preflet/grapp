from bson import json_util
from json import loads


def dump_query(q):
    return json_util.dumps(q).replace('"', "'")


def load_query(q):
    return loads(q.replace("'", '"').replace("$oid", "objectId"))