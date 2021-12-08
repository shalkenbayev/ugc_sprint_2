from loguru import logger
import logstash

from .config import settings


logstash_handler = logstash.LogstashHandler('logstash', 5044, version=1)


def request_id_filter(record):
    """Add request_id to logger data."""
    extra_fields = record.get('extra')
    request_id = extra_fields.get('request_id')
    record['request_id'] = request_id
    return True


logger.add(
    logstash_handler,
    format="api_{time:%y-%m-%d}.log",
    level=settings.log_level,
    filter=request_id_filter,
)
