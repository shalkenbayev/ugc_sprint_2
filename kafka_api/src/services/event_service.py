import typing as t

from pydantic.errors import PydanticValueError

from db.event_storage import AbstractEventProducer
from core.log_config import logger
from models.events import KafkaEvent, BaseEvent


class EventService:
    def __init__(self, event_model: t.Type[BaseEvent], producer: AbstractEventProducer):
        self.producer = producer
        self.event_model = event_model

    async def send(self, topic: str, data: list[dict]):
        kafka_events = self._make_events(data)
        await self.producer.produce(topic, kafka_events)
        return "ok"

    def _make_events(self, data: list[dict]):
        """Преобразуем полученные данные сначала в модели соответствующего топика,
         а потом в формат предназначенный для отправки в кафку"""
        kafka_events = []
        for item in data:
            try:
                event = self.event_model.parse_obj(item)
                kafka_events.append(KafkaEvent.parse_obj(event.to_event()))
            except PydanticValueError as e:
                logger.error(
                    f"Ошибка обработки входящих данных при преобразовании {item} к модели {self.event_model}\n{e}"
                )
                continue
        return kafka_events
