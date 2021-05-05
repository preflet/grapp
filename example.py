from grapp import Grapp
from load import load_from_mongodb, load_from_mysql

load_from_mongodb()
# load_from_mysql()

grapp = Grapp()
grapp.start()
