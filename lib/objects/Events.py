import sys
import os

sys.path.append('{}/../..'.format(os.path.dirname(__file__)))

from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

class Events(BaseModel):
    id: Optional[UUID] = None
    
    prospect_id: UUID
    email_id: UUID

    event_type: str
    received_at: Optional[datetime] = None

    metadata: Optional[Dict[str, Any]] = None