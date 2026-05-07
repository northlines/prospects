# db/tables.py
from sqlalchemy import MetaData
from .engine import engine

metadata = MetaData()
metadata.reflect(bind=engine)

prospects = metadata.tables["prospects"]
campaign = metadata.tables["campaign"]
emails = metadata.tables["emails"]
events = metadata.tables["events"]