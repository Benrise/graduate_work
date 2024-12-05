from fastapi import APIRouter, Depends, Request

from db.elastic import get_search_service
from utils.abstract import AsyncSearchService
from utils.enums import Indecies

router = APIRouter()


@router.post('/search')
async def search(
    request: Request,
    index: Indecies,
    body: dict = {
        "query": {
            "match_all": {}
        }
    },
    search_service: AsyncSearchService = Depends(get_search_service)
):
    result = await search_service.search(index=index, body=body)

    if result and "error" in result:
        return {"error": result["error"], "details": result["details"]}

    return result
