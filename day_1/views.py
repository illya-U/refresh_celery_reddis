from time import sleep

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

@shared_task
def add(x, y):
    sleep(3)
    return x + y
