from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('cancellation-refund/', views.cancellation_refund, name='cancellation_refund'),
    path('shipping-policy/', views.shipping_policy, name='shipping_policy'),
    path('contact-us/', views.contact_us, name='contact_us'),
]
