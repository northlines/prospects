import sys
import os

sys.path.append('{}/../..'.format(os.path.dirname(__file__)))

from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

class Prospects(BaseModel):
    id: Optional[UUID] = None

    source: Optional[str] = None
    source_url: Optional[str] = None

    entity_type: Optional[str] = None

    name: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None

    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None

    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    tiktok: Optional[str] = None
    youtube: Optional[str] = None

    address: Optional[str] = None
    city: Optional[str] = None
    zipcode: Optional[str] = None
    country: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    logo_url: Optional[str] = None
    banner_url: Optional[str] = None

    first_seen_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_contacted_at: Optional[datetime] = None

    metadata: Optional[Dict[str, Any]] = None