from django.shortcuts import render, redirect
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('book_list')
    return render(request, 'orders/create.html', {'cart': cart})
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def start_payment(request):
    amount = 50000  # paisa me (50000 = 500 INR)
    currency = "INR"
    payment_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture=1))
    payment_order_id = payment_order['id']

    return JsonResponse({
        "order_id": payment_order_id,
        "amount": amount,
        "currency": currency,
        "key": settings.RAZORPAY_KEY_ID
    })
import razorpay
from django.conf import settings
from django.shortcuts import render

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def checkout(request):
    amount = 150000  
    currency = "INR"

    payment_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture=1))
    payment_order_id = payment_order['id']

    context = {
        "order_id": payment_order_id,
        "amount": amount,
        "currency": currency,
        "key": settings.RAZORPAY_KEY_ID
    }
    return render(request, "orders/checkout.html", context)


def payment_success(request):
    payment_id = request.GET.get("payment_id", "")
    return render(request, "orders/success.html", {"payment_id": payment_id})


def payment_failed(request):
    return render(request, "orders/failed.html")
