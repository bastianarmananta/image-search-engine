from celery import Celery
from src.secret import Config

config = Config()


app = Celery(
    main="celery_app",
    broker=config.BROKER_URL,
    backend=config.BACKEND_URL,
)

app.autodiscover_tasks(["services.celery.tasks"])
