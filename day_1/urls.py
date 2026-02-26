from django.urls import path

from day_1.views import celery_test

urlpatterns = [
    path("celery_test/", celery_test)
]
