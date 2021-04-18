import asyncio
import motor.motor_asyncio

from bson import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient(
    'mongodb://root:root@a43e330d650424825a6f364729640062-823673759.eu-west-1.elb.amazonaws.com:27017/uma?authSource'
    '=admin')
db = client.uma
collection = db.infractions
query_results = []

pipelines = [[
    {'$match': {"entity": ObjectId("603247be7c0e98001c9a177e")}},
    {'$group': {"_id": "$entity", "totalInfractions": {'$sum': 1}}},
    {'$lookup': {'from': "entities", 'localField': "_id", 'foreignField': "_id", 'as': "entity_details"}},
    {'$unwind': "$entity_details"},
    {'$project': {"_id": 0, "entityId": "$_id", "fullName": "$entity_details.fullName",
                  "address": "$entity_details.address", "place": "$entity_details.place",
                  "totalInfractions": 1}},
],
    [
        {'$lookup': {'from': "components_infraction_payments", 'localField': "payment.ref", 'foreignField': "_id",
                     'as': "payment_details"}},
        {'$project': {"infractionId": "$_id", "payment": {'$arrayElemAt': ["$payment_details", 0]},
                      "entityId": "$entity"}},
        {'$group': {"_id": "$entityId", "entityId": {'$first': "$entityId"},
                    "totalInfractionPayment": {'$sum': "$payment.amount"}}}
    ],
    [
        {'$group': {"_id": "$state", "count": {'$sum': 1}}}
    ],
    [
        {"$facet":
            {
                "total": [{'$group': {'_id': 'null', 'count': {'$sum': {'$toInt': 1}}}}],
                "states": [{'$group': {"_id": "$state", "count": {'$sum': {'$toInt': 1}}}}]
            }},
        {'$unwind': "$states"},
        {'$project': {"state": "$states._id", "count": "$states.count",
                      "total": {'$arrayElemAt': ["$total.count", 0]}}},
        {'$addFields': {"percentage": {'$multiply': [{'$divide': ["$count", "$total"]}, 100]}}}
    ],
    [
        {'$unwind': "$payment"},
        {'$lookup': {'from': "components_infraction_payments", 'localField': "payment.ref", 'foreignField': "_id",
                     'as': "payment_details"}},
        {'$unwind': "$payment_details"},
        {'$group': {"_id": "$state", "amount": {'$sum': "$payment_details.amount"}}}
    ],
    [
        {'$unwind': "$payment"},
        {'$lookup': {'from': "components_infraction_payments", 'localField': "payment.ref", 'foreignField': "_id",
                     'as': "payment_details"}},
        {'$unwind': "$payment_details"},
        {'$group': {"_id": {'$dateToString': {'date': "$createdAt", 'format': "%d-%m-%Y"}}, "count": {'$sum': 1},
                    "total": {'$sum': "$payment_details.amount"}}},
        {'$match': {"_id": "26-03-2021"}}
    ],
    [
        {'$facet':
            {
                "nao":
                    [
                        {'$match': {"userPaymentId": {'$ne': 'null'}}},
                        {'$lookup': {'from': "payments", 'localField': "userPaymentId", 'foreignField': "_id",
                                     'as': "payment_details"}},
                        {'$addFields': {"startDate": "$createdAt",
                                        "endDate": {'$first': "$payment_details.updatedAt"}}},
                        {'$addFields': {
                            "days": {'$divide': [{'$subtract': ["$endDate", "$startDate"]}, 60 * 60 * 1000 * 24]}}}
                    ],
                "sim":
                    [
                        {'$match': {"xarchivedx": 'null'}},
                        {'$lookup': {'from': "components_infraction_archives", 'localField': "archive.ref",
                                     'foreignField': "_id", 'as': "archive_details"}},
                        {'$addFields': {"startDate": "$createdAt",
                                        "endDate": {'$first': "$archive_details.archiveAt"}}},
                        {'$addFields': {
                            "days": {'$divide': [{'$subtract': ["$endDate", "$startDate"]}, 60 * 60 * 1000 * 24]}}}
                    ]
            }
        },
        {'$project': {"details": {'$setUnion': ["$nao", "$sim"]}}}, {'$unwind': '$details'},
        {'$replaceRoot': {'newRoot': "$details"}},
        {'$group': {"_id": 'null', "averageDays": {'$avg': "$days"}}}

    ]
]


async def f():
    for pipeline in pipelines:
        list_element = []
        async for doc in collection.aggregate(pipeline):
            print(doc)
            list_element.append(doc)
        print("Pipeline Ended")
        query_results.append(list_element)


loop = asyncio.get_event_loop()
loop.run_until_complete(f())
print(query_results)
