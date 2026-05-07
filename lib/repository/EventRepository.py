import sys
import os

sys.path.append('{}/../..'.format(os.path.dirname(__file__)))

from sqlalchemy import select, update, exists, and_, not_, or_, desc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func
from sqlalchemy import text

from typing import Optional
from lib.objects.Events import Events
from typing import List
from uuid import UUID
from datetime import datetime, timedelta

from core.exceptions import AppException

from lib.db.tables import (
    events
)

class EventRepository:
    @staticmethod
    def insertEvent(session, event:Events) -> Events:
        stmt = (
            insert(events)
            .values(**event.model_dump(
                    exclude_none=True, 
                    exclude_unset=True,
                    exclude={"id", "received_at"}
                )
            )
            .returning(*events.c)
        )
        
        row = session.execute(stmt).mappings().one()
        return Events.model_validate(row)