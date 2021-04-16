import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://root:root@a43e330d650424825a6f364729640062-823673759'
                                                    '.eu-west-1.elb.amazonaws.com:27017/uma')
db = client.uma
collection = db.vehicles
