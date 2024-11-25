#/!bin/bash

celery -A service.celery.app worker --loglevel=INFO
