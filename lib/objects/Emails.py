import sys
import os

sys.path.append('{}/../..'.format(os.path.dirname(__file__)))

from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

class Emails(BaseModel):
    id: Optional[UUID] = None
    
    prospect_id: Optional[UUID] = None
    campaign_id: Optional[UUID] = None

    to_addr: str
    from_addr: str
    sent_at: Optional[datetime] = None

    subject: str
    content: str
    
    brevo_id: str