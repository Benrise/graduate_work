import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from api.v1 import search
from core.config import settings
from core.logger import LOGGING
from db import redis
from db.redis import RedisCacheAdapter
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from managers.lifespan import LifespanManager
from redis.asyncio import Redis
from utils.logger import logger
from utils.scheduler import scheduler


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)
    cache_adapter = RedisCacheAdapter(redis.redis)
    lifespan_manager = LifespanManager(cache=cache_adapter)

    asyncio.create_task(
        scheduler(
            lifespan_manager.update_data_titles,
            settings.titles_update_interval
        )
    )
    await lifespan_manager.upload_ner_model()
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
