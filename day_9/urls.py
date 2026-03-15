from django.urls import path

from day_9.views import celery_test, celery_test_with_ack, celery_task_send_to_two_queues

urlpatterns = [
    path("celery_test/", celery_test),
    path("celery_test_with_ack/", celery_test_with_ack),
    path("celery_task_send_to_two_queues/", celery_task_send_to_two_queues)
]