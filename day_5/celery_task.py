from billiard.exceptions import SoftTimeLimitExceeded
from celery import shared_task

from day_5.services.PaymentService import PaymentService


@shared_task(bind=True, max_retries=3, soft_time_limit=30)
def pay_order(self, payment_id):
    try:
        PaymentService().pay_order(payment_id)
    except SoftTimeLimitExceeded:
        print("!!!SoftTimeLimitExceeded!!!")
        raise self.retry(countdown=1)
