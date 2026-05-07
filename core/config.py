import os
import uuid
from datetime import timedelta
from dotenv import dotenv_values

class Config:
    config = {
        **dotenv_values('{}/../.env'.format(os.path.dirname(__file__))),  # load development variables
        **os.environ,  # override loaded values with environment variables
    }

    DB_NAME = config.get("POSTGRES_DB")
    DB_USER = config.get("POSTGRES_USER")
    DB_PASSWORD = config.get("POSTGRES_PASSWORD")
    DB_HOST = config.get("PSQL_HOST")
    DB_PORT = config.get("PSQL_PORT")
    BREVO_KEY = config.get("BREVO_API")
    
    SECRET_KEY = config.get("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY not set")
    
    LOG_DIR = config.get("LOG_DIR")
    if not LOG_DIR:
        LOG_DIR = './.log'
        
    SERVICE_NAME = config.get("SERVICE_NANE")
    if not SERVICE_NAME:
        SERVICE_NAME = f'Uknown-{uuid.uuid4().hex}'
    else:
        SERVICE_NAME = f'{SERVICE_NAME}-{uuid.uuid4().hex}'