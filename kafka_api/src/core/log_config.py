from loguru import logger

from .config import settings

logger.add(
    "api_{time:%y-%m-%d}.log",
    level=settings.log_level
)
