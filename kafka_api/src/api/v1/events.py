from fastapi import APIRouter, Depends

from core.config import settings
from core.di import DI
from models.events import MovieWatchProgressEvent
from services.event_service import EventService

event_api = APIRouter()


@event_api.post(
    "/watch_movie",
    response_model=str,
    summary="Отправка событий в kafka данных о просмотре фильмов",
    description="Отправка данных о просмотре фильмов",
    tags=["Movie Events"],
)
async def watch_movie(data: list[MovieWatchProgressEvent], event_service: EventService = Depends(DI.get_movie_service)):
    return await event_service.send(settings.movie_events_topic, data)
