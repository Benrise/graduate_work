import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import Field
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = Field(..., alias='ASSISTANT_PROJECT_NAME')
    service_host: str = Field('assistant', alias='ASSISTANT_SERVICE_HOST')
    service_port: int = Field(8004, alias='ASSISTANT_SERVICE_PORT')
    debug: bool = Field(True, alias='ASSISTANT_DEBUG')


settings = Settings()


class ELKSettings(BaseSettings):
    logstash_host: str = Field(..., alias='ELK_LOGSTASH_HOST')
    logstash_port: int = Field(..., alias='ELK_LOGSTASH_PORT')


elk_settings = ELKSettings()
