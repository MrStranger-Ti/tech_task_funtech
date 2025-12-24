import taskiq_fastapi
from fastapi import FastAPI
from taskiq_aio_kafka import AioKafkaBroker

from app.core.settings import settings

broker = AioKafkaBroker(bootstrap_servers=settings.broker.KAFKA_URL)


def configure_tasks_dependencies(app: FastAPI) -> None:
    taskiq_fastapi.init(broker, app)


# importing all tasks
from app.orders.infrastructure.broker.tasks import create_order_task
