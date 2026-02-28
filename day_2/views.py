from time import sleep

from asgiref.timeout import timeout
from celery import shared_task
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def celery_test(request):
    celery_task = add.delay(2, 3)
    print(celery_task.status)
    value = celery_task.get()
    print(value)
    value = "wait"

    return JsonResponse(data={"value": value}, status=200)


@csrf_exempt
def celery_test_with_ack(request):
    celery_task = add_with_ack.delay(2, 3)
    value = celery_task.get()

    return JsonResponse(data={"value": value}, status=200)


@shared_task(bind=True, max_retries=3)
def add(self, x, y):
    print("self.request", self.request)
    print("self.request.id", self.request.id)
    print("self.max_retries", self.max_retries)
    print("self.request.retries", self.request.retries)
    if self.request.retries != 3:
        raise self.retry(exc="wow", countdown=1)
    return self.request.retries


@shared_task(bind=True, max_retries=3)
def add_with_ack(self, x, y):
    print("sss")
    sleep(200)
    raise 10/0
