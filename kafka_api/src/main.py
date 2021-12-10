import os
import uuid

import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request
from loguru import logger
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from api.v1.events import event_api
from api.v1.user_events import user_event
from core.config import settings
from core.di import DI
from services.event_service import EventService

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    traces_sample_rate=1.0,
)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)


@app.middleware("http")
async def log_middle(request: Request, call_next):
    """Middleware to append request_id to logs extra data."""
    request_id = request.headers.get('X-Request-Id', str(uuid.uuid4()))
    config = {"extra": {"request_id": request_id}}
    logger.configure(**config)
    response = await call_next(request)
    return response


try:
    app.add_middleware(SentryAsgiMiddleware)
except Exception as error:
    logger.error(f'Sentry integration failed, error - {error}')

app.include_router(event_api, prefix="/api/v1/events")
app.include_router(user_event, prefix="/api/v1/events")


@app.on_event("startup")
async def startup():
    movie_service: EventService = await DI.get_movie_service()
    await movie_service.producer.start()


@app.on_event("shutdown")
async def shutdown():
    movie_service: EventService = await DI.get_movie_service()
    await movie_service.producer.stop()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
