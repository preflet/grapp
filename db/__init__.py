import hermes.backend.dict
import os
import sys
from dotenv import load_dotenv

extDataDir = os.getcwd()
if getattr(sys, 'frozen', False):
    extDataDir = sys._MEIPASS

load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

DB_TTL = 10 * 60
cache = hermes.Hermes(hermes.backend.dict.Backend, ttl=DB_TTL)
