import sys
import os

sys.path.append('{}/../..'.format(os.path.dirname(__file__)))

# db/engine.py
from sqlalchemy import create_engine
from lib.db.config import Config

engine = create_engine(
    Config.DB_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    future=True
)