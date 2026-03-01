from django.db import transaction
from rest_framework.exceptions import ValidationError

from day_5.models import ProviderType, Payment, Order, PaymentStatus, OrderStatus
from day_5.payment_provider import FakeProvider, StripePaymentProvider

PAYMENT_PROVIDER_TYPE_TO_PAYMENT_PROVIDER = {
    ProviderType.FAKE_PROVIDER: FakeProvider,
    ProviderType.STRIPE: StripePaymentProvider,
}


class PaymentService:
    def pay_order(self, payment_id):
        with transaction.atomic():
            payment = Payment.objects.select_for_update().select_related("order").get(pk=payment_id)
            order = Order.objects.select_for_update().get(pk=payment.order.id)
            self._pay_business_validation(payment, order)
            payment.status = PaymentStatus.PROCESSING
            payment.save()

            payment_provider_class = PAYMENT_PROVIDER_TYPE_TO_PAYMENT_PROVIDER[payment.provider]
            operation_status = payment_provider_class().pay(payment.amount)

        with transaction.atomic():
            payment = Payment.objects.select_for_update().select_related("order").get(pk=payment_id)
            order = Order.objects.select_for_update().get(pk=payment.order.id)

            if operation_status:
                payment.status = PaymentStatus.SUCCESS
                order.status = OrderStatus.PAID
            else:
                payment.status = PaymentStatus.FAILED

            print("___PAYMENT___")
            payment.save()
            order.save()
        return payment

    def _pay_business_validation(self, payment, order):
        if payment.status != PaymentStatus.PENDING:
            print("!!!Only pending payment can be paid!!!")
            raise ValidationError("Only pending payment can be paid.")

        if order.status != OrderStatus.PENDING:
            print("!!!Failed order can't be paid.!!!")
            raise ValidationError("Failed order can't be paid.")

        return payment

    def cancel_payment(self, payment_id):
        with transaction.atomic():
            payment = Payment.objects.select_for_update().get(pk=payment_id)
            self._business_validation_cancel(payment)
            self._cancel_order(payment)
        return payment

    def _business_validation_cancel(self, payment):
        if payment.status != PaymentStatus.PENDING:
            raise ValidationError("Only pending payment can be cancelled.")

        return payment

    def _cancel_order(self, payment):
        payment.status = PaymentStatus.FAILED
        payment.save()
