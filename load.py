import dask.dataframe as dd
from db.mongodb import Mongo
from db.mysqldb import SQL
import pandas as pd


def load_from_file(path):
    ddf = dd.read_csv(path)
    return ddf


def load_from_file_creds(credentials):
    path = credentials['path']
    ddf = dd.read_csv(path)
    print(ddf)
    return ddf


def load_from_mongodb(credentials):
    mongo = Mongo(credentials)
    result = mongo.get_result_and_cache()
    print(result)


def load_from_mysql(credentials):

    sql = SQL(credentials)
    result = sql.get_result_and_cache()
    df = pd.DataFrame(result)
    # df.columns = ["created_date","year_week","date_m","time_m"]
    print(df.head())


load_from = {'mongo': load_from_mongodb,
             'mysql': load_from_mysql,
             'file': load_from_file_creds}
