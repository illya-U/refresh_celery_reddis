import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "refresh_celery_reddis.settings")

app = Celery("refresh_celery_reddis")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()