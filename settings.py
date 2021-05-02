from dotenv import load_dotenv

import os

load_dotenv('.env')
URI_MONGODB = os.getenv('URI_MONGODB')
HOST_MYSQL = os.getenv('HOST_MYSQL')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
