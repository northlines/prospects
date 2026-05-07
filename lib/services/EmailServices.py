from uuid import UUID
from typing import List, Optional

from lib.db.session import db_session
from lib.repository.EmailRepository import EmailRepository

from core.logger import get_logger
from core.exceptions import AppException

from lib.objects.Emails import Emails

class EmailServices:

    @staticmethod
    def register(email:Emails) -> Emails:
        with db_session() as session:
            r = EmailRepository.insertEmail(session, email)
            return r

    @staticmethod
    def getByBrevoId(brevo_id:str) -> Emails:
        with db_session() as session:
            p = EmailRepository.getByBrevoId(session, brevo_id)
            return p