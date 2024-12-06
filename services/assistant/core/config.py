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
    search_service_host: str = Field('search', alias='API_SERVICE_HOST')
    search_service_port: int = Field(8002, alias='API_SERVICE_PORT')
    titles_update_interval: int = Field(30, alias='ASSISTANT_TITLES_UPDATE_INTERVAL_MINUTES')
    titles_films_cache_key: str = 'search:films_titles'
    titles_genres_cache_key: str = 'search:genres_titles'
    redis_host: str = Field('redis', alias='ASSISTAN_REDIS_HOST')
    redis_port: int = Field(6379, alias='ASSISTANT_REDIS_PORT')
    debug: bool = Field(True, alias='ASSISTANT_DEBUG')

    @property
    def search_service_url(self):
        return f"http://{self.search_service_host}:{self.search_service_port}"


settings = Settings()


class ELKSettings(BaseSettings):
    logstash_host: str = Field(..., alias='ELK_LOGSTASH_HOST')
    logstash_port: int = Field(..., alias='ELK_LOGSTASH_PORT')


elk_settings = ELKSettings()
