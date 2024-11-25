#/!bin/bash

celery -A services.celery.app worker --loglevel=INFO
