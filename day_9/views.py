from time import sleep

from celery import shared_task
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from refresh_celery_reddis.celery import app


@csrf_exempt
def celery_test(request):
    celery_task = add.delay(2, 3)
    print(celery_task.status)
    value = celery_task.get()
    value = "wait"

    return JsonResponse(data={"value": value}, status=200)


@csrf_exempt
def celery_test_with_ack(request):
    celery_task = add_with_ack.delay(2, 3)
    value = celery_task.get()

    return JsonResponse(data={"value": value}, status=200)


@app.task(rate_limit="1/m", bind=True, max_retries=3)
def add(self, x, y):
    print("self.request", self.request)
    print("self.request.id", self.request.id)
    print("self.max_retries", self.max_retries)
    print("self.request.retries", self.request.retries)
    return self.request.retries


@shared_task(bind=True, max_retries=3)
def add_with_ack(self, x, y):
    print("sss")
    sleep(200)
    raise 10/0


# change on command: celery -A refresh_celery_reddis worker --loglevel=info -Q high_priority,default
# for work
@csrf_exempt
def celery_task_send_to_two_queues(request):
    priority_task = add_with_ack.apply_async(args=[2, 3], queue="high_priority")
    default_task_0 = add_with_ack.apply_async(args=[2, 3], queue="default")
    default_task_1 = add_with_ack.apply_async(args=[2, 3], queue="default")
    default_task_2 = add_with_ack.apply_async(args=[2, 3], queue="default")
    default_task_3 = add_with_ack.apply_async(args=[2, 3], queue="default")

    return JsonResponse(data=
        {
            "priority_task.status": priority_task.status,
            "default_task_0": default_task_0.status,
            "default_task_1": default_task_1.status,
            "default_task_2": default_task_2.status,
            "default_task_3": default_task_3.status,
        }
    )







# Create your views here.
