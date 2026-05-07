import time
import sys
import os

sys.path.append('{}/../..'.format(os.path.dirname(__file__)))

from sqlalchemy import create_engine, text
from lib.db.config import Config

def wait_for_db(max_retries=30, delay=2):
    engine = create_engine(Config.DB_URL)

    try:
        for attempt in range(max_retries):
            try:
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                print("✅ Database is ready")
                return
            
            except Exception:
                print(f"⏳ Waiting for DB... ({attempt+1}/{max_retries})")
                time.sleep(delay)

        raise Exception("❌ Database not available after retries")

    finally:
        engine.dispose()