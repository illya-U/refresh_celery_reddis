from django.urls import path
from rest_framework.generics import RetrieveAPIView

from day_5.views import OrdersApiView, OrdersRetrieveApiView, CancelOrderApiView, PaymentsApiView, \
    PaymentRetrieveApiView, PayPaymentApiView, CancelPaymentApiView, PaymentLogsListApiView, RegisterAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name="registers"),
    path('orders/', OrdersApiView.as_view(), name="orders"),
    path('orders/<int:pk>/', OrdersRetrieveApiView.as_view(), name="order_details"),
    path("orders/<int:pk>/cancel/", CancelOrderApiView.as_view(), name="cancel_order"),

    path('payments/', PaymentsApiView.as_view(), name='payments'),
    path('payments/<int:fk>/', PaymentRetrieveApiView.as_view(), name='payment_details'),

    path("payments/<int:pk>/pay/", PayPaymentApiView.as_view(), name="pay_order"),
    path("payments/<int:pk>/cancel/", CancelPaymentApiView.as_view(), name="cancel_order"),
    path('payment_logs/', PaymentLogsListApiView.as_view(), name='payment_logs'),
]
