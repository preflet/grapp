import hermes.backend.dict
from dotenv import load_dotenv

load_dotenv('../.env')
DB_TTL = 10 * 60
cache = hermes.Hermes(hermes.backend.dict.Backend, ttl=DB_TTL)
