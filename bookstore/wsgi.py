import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE','bookstore.settings')
application=get_wsgi_application()
import razorpay
from django.conf import settings
from django.http import JsonResponse

def start_payment(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    DATA = {
        "amount": 50000,  
        "currency": "INR",
        "payment_capture": 1
    }

    order = client.order.create(data=DATA)
    return JsonResponse(order)
