# db/session.py
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from .engine import engine

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@contextmanager
def db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()