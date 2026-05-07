import sys
import os

sys.path.append('{}/../..'.format(os.path.dirname(__file__)))

from sqlalchemy import select, update, exists, and_, not_, or_, desc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func
from sqlalchemy import text

from typing import Optional
from lib.objects.Emails import Emails
from typing import List
from uuid import UUID
from datetime import datetime, timedelta

from core.exceptions import AppException

from lib.db.tables import (
    emails
)

class EmailRepository:
    @staticmethod
    def insertEmail(session, email:Emails) -> Emails:
        stmt = (
            insert(emails)
            .values(**email.model_dump(
                    exclude_none=True, 
                    exclude_unset=True,
                    exclude={"id", "sent_at"}
                )
            )
            .returning(*emails.c)
        )
        
        row = session.execute(stmt).mappings().one()
        return Emails.model_validate(row)

    @staticmethod
    def getByBrevoId(session, brevo_id:str) -> Emails:
        stmt = (
            select(emails)
            .where(emails.c.brevo_id == brevo_id)
        )
        row = session.execute(stmt).mappings().first()

        if not row:
            raise AppException(
                message=f'Email ({id}) does not exist',
                code="EMAIL_NOT_FOUND",
                status=404
            )

        return Emails.model_validate(row)