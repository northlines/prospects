
import sys
import os

sys.path.append('{}/../..'.format(os.path.dirname(__file__)))

from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

class Emails(BaseModel):
    id: Optional[UUID] = None
    
    name: str
    template: str

    created_at: Optional[datetime] = None