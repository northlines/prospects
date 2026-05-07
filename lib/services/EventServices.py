from uuid import UUID
from typing import List, Optional

from lib.db.session import db_session
from lib.repository.EventRepository import EventRepository

from core.logger import get_logger
from core.exceptions import AppException

from lib.objects.Events import Events

class EventServices:

    @staticmethod
    def register(event:Events) -> Events:
        with db_session() as session:
            r = EventRepository.insertEvent(session, event)
            return r