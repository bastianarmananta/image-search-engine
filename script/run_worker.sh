#/!bin/bash

CELERY_WORKER_PATH="$PWD/services/celery/worker.py"

if [ ! -f "$CELERY_WORKER_PATH" ]; then
    echo "Celery worker not found!"
    exit 1
fi

echo "Worker file found. Standby processing request..."
celery -A services.celery.worker worker --loglevel=INFO
