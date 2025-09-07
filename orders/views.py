from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import razorpay

from cart.cart import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm

# Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Helper - shipping cost
def _calc_shipping(subtotal: Decimal) -> Decimal:
    return Decimal("0.00") if subtotal >= Decimal("499.00") else Decimal("49.00")

# ✅ Checkout (Amazon style)
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect("shop:book_list")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            # totals
            subtotal = Decimal(cart.get_total_price())
            shipping = _calc_shipping(subtotal)
            total = subtotal + shipping
            order.subtotal = subtotal
            order.shipping = shipping
            order.total = total
            order.save()

            # order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    book=item["book"],
                    price=Decimal(item["price"]),
                    quantity=item["quantity"],
                )

            # Razorpay order
            amount_paise = int(total * 100)
            rzp_order = razorpay_client.order.create(dict(amount=amount_paise, currency="INR", payment_capture=1))
            order.razorpay_order_id = rzp_order["id"]
            order.save(update_fields=["razorpay_order_id"])

            context = {
                "order": order,
                "cart": cart,
                "rzp_key": settings.RAZORPAY_KEY_ID,
                "amount_paise": amount_paise,
            }
            return render(request, "orders/checkout.html", context)
    else:
        form = CheckoutForm()

    return render(request, "orders/create.html", {"form": form, "cart": cart})


# ✅ Payment success
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        rzp_order_id   = request.POST.get("razorpay_order_id")
        rzp_payment_id = request.POST.get("razorpay_payment_id")
        rzp_signature  = request.POST.get("razorpay_signature")

        order = get_object_or_404(Order, razorpay_order_id=rzp_order_id)

        params_dict = {
            'razorpay_order_id': rzp_order_id,
            'razorpay_payment_id': rzp_payment_id,
            'razorpay_signature': rzp_signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            order.paid = True
            order.razorpay_payment_id = rzp_payment_id
            order.razorpay_signature = rzp_signature
            order.save(update_fields=["paid", "razorpay_payment_id", "razorpay_signature"])
            Cart(request).clear()
            return render(request, "orders/success.html", {"order": order})
        except razorpay.errors.SignatureVerificationError:
            return render(request, "orders/failed.html", {"message": "Signature verification failed"})

    return redirect("orders:order_create")


# ✅ Payment failed
def payment_failed(request):
    return render(request, "orders/failed.html")
