import uvicorn
import logging
import asyncio

from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

from core.config import settings
from core.logger import LOGGING
from dependencies.extractor import update_data_titles
from utils.logger import logger
from utils.scheduler import scheduler
from api.v1 import search


@asynccontextmanager
async def lifespan(_: FastAPI):
    asyncio.create_task(
        scheduler(
            update_data_titles,
            settings.titles_update_interval
        )
    )
    yield

app = FastAPI(
    title=settings.project_name,
    docs_url='/assistant/api/v1/docs',
    openapi_url='/assistant/api/v1/docs.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


@app.middleware('http')
async def before_request(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': 'X-Request-Id is required'})

    logger.info(
        "middleware",
        extra={
            "request_id": request_id,
            "host": settings.service_host,
            "method": request.method,
            "query_params": str(request.query_params),
            "status_code": response.status_code,
            "elapsed_time": (datetime.now() - start_time).total_seconds(),
        }
    )

    return response


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


app.include_router(search.router, prefix='/assistant/api/v1/search', tags=['search'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.service_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
