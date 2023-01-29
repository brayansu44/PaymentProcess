from django.urls import path
from .views import PaymentListCreateAPIView, PaymentRetrieveUpdateDestroyAPiView

urlpatterns = [
    path('api/payment-tc/process/', PaymentListCreateAPIView.as_view(), name = 'payment_list'),
    path('api/payment-tc/process/<int:pk>/', PaymentRetrieveUpdateDestroyAPiView.as_view(), name = 'payment_retrieve'),
]


