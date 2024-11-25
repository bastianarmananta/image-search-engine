import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from celery import Celery
from src.secret import Config

config = Config()
BROKER_URL = f"amqp://{config.RABBITMQ_DEFAULT_USER}:{config.RABBITMQ_DEFAULT_PASS}@{config.RABBITMQ_DEFAULT_HOST}"

app = Celery(
    "testing_celery",
    broker=f"{BROKER_URL}",
    backend="rpc://",
)
