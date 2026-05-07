from uuid import UUID
from typing import List, Optional

from lib.db.session import db_session
from lib.repository.ProspectsRepository import ProspectsRepository

from core.logger import get_logger
from core.exceptions import AppException

from lib.objects.Prospects import Prospects

class ProspectsServices:

    @staticmethod
    def register(prospect:Prospects) -> Prospects:
        with db_session() as session:
            r = ProspectsRepository.insertProspect(session, prospect)
            return r

    @staticmethod
    def get(id:UUID) -> Prospects:
        with db_session() as session:
            p = ProspectsRepository.getProspect(session, id)
            return p
    
    def unsubscribe(id:UUID, unsubscribe: bool = True) -> Prospects:
        with db_session() as session:
            p = ProspectsRepository.setProspectUnsubscribed(session, id, unsubscribe)
            return p