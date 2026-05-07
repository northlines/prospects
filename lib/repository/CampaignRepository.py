import sys
import os

sys.path.append('{}/../..'.format(os.path.dirname(__file__)))

from sqlalchemy import select, update, exists, and_, not_, or_, desc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func
from sqlalchemy import text

from typing import Optional
from lib.objects.Campaign import Campaign
from lib.objects.Prospects import Prospects
from typing import List
from uuid import UUID
from datetime import datetime, timedelta

from core.exceptions import AppException

from lib.db.tables import (
    campaign,
    emails,
    prospects
)

class CampaignRepository:
    @staticmethod
    def insertCampaign(session, c:Campaign) -> Campaign:
        stmt = (
            insert(campaign)
            .values(**c.model_dump(
                    exclude_none=True, 
                    exclude_unset=True,
                    exclude={"id", "created_at"}
                )
            )
            .returning(*campaign.c)
        )
        
        row = session.execute(stmt).mappings().one()
        return Campaign.model_validate(row)

    @staticmethod
    def getCampaignByName(session, name:str) -> Campaign:
        stmt = (
            select(campaign)
            .where(campaign.c.name == name)
        )
        row = session.execute(stmt).mappings().first()

        if not row:
            raise AppException(
                message=f'Campaign ({id}) does not exist',
                code="CAMPAIGN_NOT_FOUND",
                status=404
            )

        return Campaign.model_validate(row)

    @staticmethod
    def getProspectForCampaign(session, campaign_name: str) -> Prospects:
        subquery = (
            select(emails.c.id)
            .join(campaign, campaign.c.id == emails.c.campaign_id)
            .where(
                emails.c.prospect_id == prospects.c.id,
                campaign.c.name == campaign_name
            )
        )

        stmt = (
            select(prospects)
            .where(~exists(subquery))
            .order_by(func.random())
            .limit(1)
        )

        row = session.execute(stmt).mappings().first()

        if not row:
            raise AppException(
                message="No available prospect for campaign 'coldemail'",
                code="NO_PROSPECT_AVAILABLE",
                status=404
            )

        return Prospects.model_validate(row)