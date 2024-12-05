from core.config import settings
from services.search import SearchService


def get_search_service():
    return SearchService(settings.search_service_url)
