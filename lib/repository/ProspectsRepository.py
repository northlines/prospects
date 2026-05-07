import sys
import os

sys.path.append('{}/../..'.format(os.path.dirname(__file__)))

from sqlalchemy import select, update, exists, and_, not_, or_, desc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func
from sqlalchemy import text

from typing import Optional
from lib.objects.Prospects import Prospects
from typing import List
from uuid import UUID
from datetime import datetime, timedelta

from core.exceptions import AppException

from lib.db.tables import (
    prospects
)

class ProspectsRepository:
    @staticmethod
    def insertProspect(session, prospect:Prospects) -> Prospects:
        stmt = (
            insert(prospects)
            .values(**prospect.model_dump(
                    exclude_none=True, 
                    exclude_unset=True,
                    exclude={"id", "first_seen_at","updated_at","last_contacted_at"}
                )
            )
            .returning(*prospects.c)
        )
        
        row = session.execute(stmt).mappings().one()
        return Prospects.model_validate(row)

    @staticmethod
    def getProspect(session, id:UUID) -> Prospects:
        stmt = (
            select(prospects)
            .where(prospects.c.id == id)
        )
        row = session.execute(stmt).mappings().first()

        if not row:
            raise AppException(
                message=f'Prospect ({id}) does not exist',
                code="PROSPECT_NOT_FOUND",
                status=404
            )

        return Prospects.model_validate(row)
    
    @staticmethod
    def setProspectUnsubscribed(
        session,
        id: UUID,
        unsubscribed: bool
    ) -> Prospects:

        stmt = (
            update(prospects)
            .where(prospects.c.id == id)
            .values(
                unsubscribed=unsubscribed
            )
            .returning(*prospects.c)
        )

        row = session.execute(stmt).mappings().first()

        if not row:
            raise AppException(
                message=f'Prospect ({id}) does not exist',
                code="PROSPECT_NOT_FOUND",
                status=404
            )

        session.commit()

        return Prospects.model_validate(row)