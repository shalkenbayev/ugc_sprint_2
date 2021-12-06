import uvicorn
from fastapi import FastAPI

from api.v1.events import event_api
from core.config import settings
from core.di import DI
from services.event_service import EventService


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

app.include_router(event_api, prefix="/api/v1/events")


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
