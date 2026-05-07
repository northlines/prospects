from uuid import UUID
from typing import List, Optional
from jinja2 import Template

from lib.db.session import db_session
from lib.repository.CampaignRepository import CampaignRepository

from core.logger import get_logger
from core.exceptions import AppException

from lib.objects.Campaign import Campaign
from lib.objects.Prospects import Prospects

class CampaignServices:

    @staticmethod
    def register(c:Campaign) -> Campaign:
        with db_session() as session:
            r = CampaignRepository.insertCampaign(session, c)
            return r

    @staticmethod
    def getCampaign(name:str) -> Campaign:
        with db_session() as session:
            p = CampaignRepository.getCampaignByName(session, name)
            return p
        
    @staticmethod
    def getProspectForCampaign(name: str) -> Prospects:
        with db_session() as session:
            p = CampaignRepository.getProspectForCampaign(session, name)
            return p

    @staticmethod
    def formatEmail(campaign_name:str, prospect: Prospects):
        c = CampaignServices.getCampaign(campaign_name)

        print(c.subject)

        s_template = Template(c.subject)
        subject = s_template.render(**prospect.model_dump())

        e_template = Template(c.template)
        email = e_template.render(**prospect.model_dump())

        return subject, email