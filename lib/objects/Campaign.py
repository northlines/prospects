
import sys
import os

sys.path.append('{}/../..'.format(os.path.dirname(__file__)))

from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

class Campaign(BaseModel):
    id: Optional[UUID] = None
    
    name: str
    template: str
    subject: str

    created_at: Optional[datetime] = None