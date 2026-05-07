import sys
import os

sys.path.append('{}/../..'.format(os.path.dirname(__file__)))

from urllib.parse import quote_plus
from core.config import Config

class Config:

    DB_NAME = Config.DB_NAME
    DB_USER = Config.DB_USER
    DB_PASSWORD = quote_plus(Config.DB_PASSWORD)
    DB_HOST = Config.DB_HOST
    DB_PORT = Config.DB_PORT

    DB_URL = (
        f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    print(DB_URL)