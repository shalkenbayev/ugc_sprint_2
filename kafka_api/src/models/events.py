import typing as t

from pydantic import BaseModel


class KafkaEvent(BaseModel):
    """Модель событий отправляемых для кафки"""
    key: t.Optional[bytes] = None
    value: bytes


class BaseEvent(BaseModel):
    """Определяем свой базовый класс с новыми методами"""
    def to_event(self):
        raise NotImplementedError


class MovieWatchProgressEvent(BaseEvent):
    """Модель входящих данных для формирования события о прогрессе просмотра фильма пользователем
    user_id: идентификатор пользователя
    movie_id: идентификатор фильма
    viewed_frame: временная отметка прогресса просмотра фильма
    """
    user_id: str
    movie_id: str
    viewed_frame: str

    def to_event(self):
        """Метод для трансформации полученных данных в модель event, для последующей отправки в кафку"""
        key = f"{self.user_id}:{self.movie_id}".encode("utf-8")
        value = self.viewed_frame.encode("utf-8")
        return KafkaEvent(key=key, value=value)
