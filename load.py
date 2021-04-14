import dask.dataframe as dd

def load_from_file(path):
    ddf = dd.read_csv(path)
    return ddf


def load_from_db():
    pass

