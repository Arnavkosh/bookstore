import stripe
from django.conf import settings
from django.shortcuts import redirect,render
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import HttpResponse
from orders.models import Order

def create_checkout_session(request):
    order_id=request.session.get('order_id')
    if not order_id:
        return redirect('/cart/')
    order=Order.objects.get(id=order_id)
    stripe.api_key=settings.STRIPE_SECRET_KEY
    line_items=[{{'price_data':{{'currency':settings.CURRENCY,'product_data':{{'name':item.product}},'unit_amount':int(item.price*100)}},'quantity':item.quantity}} for item in order.items.all()]
    session=stripe.checkout.Session.create(payment_method_types=['card'],mode='payment',line_items=line_items,success_url=request.build_absolute_uri(reverse('payment:success'))+'?session_id={CHECKOUT_SESSION_ID}',cancel_url=request.build_absolute_uri(reverse('payment:cancel')),metadata={{'order_id':str(order.id)}})
    order.stripe_payment_intent=session.payment_intent
    order.save()
    return redirect(session.url,code=303)

def success(request):
    return render(request,'payment/success.html')

def cancel(request):
    return render(request,'payment/cancel.html')

@csrf_exempt
def webhook(request):
    payload=request.body
    sig_header=request.META.get('HTTP_STRIPE_SIGNATURE')
    stripe.api_key=settings.STRIPE_SECRET_KEY
    endpoint_secret=settings.STRIPE_WEBHOOK_SECRET
    try:
        event=stripe.Webhook.construct_event(payload=payload,sig_header=sig_header,secret=endpoint_secret)
    except Exception:
        return HttpResponse(status=400)
    if event['type']=='checkout.session.completed':
        session=event['data']['object']
        order_id=session.get('metadata',{{}}).get('order_id')
        if order_id:
            order=Order.objects.filter(id=order_id).first()
            if order:
                order.paid=True
                order.save()
    return HttpResponse(status=200)
