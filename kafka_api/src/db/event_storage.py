import asyncio
import random
from abc import ABC, abstractmethod

from aiokafka import AIOKafkaProducer

from core.config import settings
from core.log_config import logger
from models.events import KafkaEvent


class AbstractEventProducer(ABC):
    """Абстрактный класс - интерфейс producer для хранилища событий. Например Kafka"""

    @abstractmethod
    async def start(self):
        raise NotImplementedError

    @abstractmethod
    async def stop(self):
        raise NotImplementedError

    @abstractmethod
    async def produce(self, topic: str, events: list[KafkaEvent]):
        raise NotImplementedError


class KafkaProducerAIO(AbstractEventProducer):
    """Класс реализация отправки событий в кафку, с использованием асинхронной библиотеки `aiokafka`"""
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.producer = AIOKafkaProducer(loop=loop, bootstrap_servers=settings.kafka_bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def produce(self, topic: str, events: list[KafkaEvent]):
        """Формируем батчи и отправляем их в кафку на рандомно выбранные партиции топика"""
        batch = self.producer.create_batch()
        for event in events:
            metadata = batch.append(key=event.key, value=event.value, timestamp=None)
            if metadata is None:
                await self._flush(batch, topic)
                batch = self.producer.create_batch()
                continue
        if batch.record_count != 0:
            await self._flush(batch, topic)

    async def _flush(self, batch, topic):
        partitions = await self.producer.partitions_for(topic)
        partition = random.choice(tuple(partitions))
        await self.producer.send_batch(batch, topic, partition=partition)
        logger.debug(f"Send {batch.record_count()} events to partition: {partition}")
