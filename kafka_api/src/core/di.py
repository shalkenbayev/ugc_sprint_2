from functools import partial

from db.event_storage import KafkaProducerAIO
from models.events import MovieWatchProgressEvent
from services.event_service import EventService


class DI:

    service_instances = {}

    @classmethod
    async def get_movie_service(cls):
        return await partial(cls._get_service, service_cls="movie_service", event_model=MovieWatchProgressEvent)()

    @classmethod
    async def _get_service(cls, service_cls, event_model):
        """Делаем сервисы синглтонами"""
        if service_cls in cls.service_instances:
            service = cls.service_instances[service_cls]
        else:
            cls.service_instances[service_cls] = EventService(
                event_model=event_model, producer=KafkaProducerAIO()
            )
            service = cls.service_instances[service_cls]
        return service
