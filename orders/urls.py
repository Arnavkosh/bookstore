
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('pay/', views.start_payment, name='start_payment'),
]
from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.payment_success, name="payment_success"),
    path("failed/", views.payment_failed, name="payment_failed"),
]
