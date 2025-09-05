from django.shortcuts import render,redirect
from .forms import OrderCreateForm
from .models import Order,OrderItem
from cart.cart import Cart

def order_create(request):
    cart=Cart(request)
    if request.method=='POST':
        form=OrderCreateForm(request.POST)
        if form.is_valid() and len(cart)>0:
            order=Order.objects.create(**form.cleaned_data)
            for item in cart:
                OrderItem.objects.create(order=order,product=item['book'].title,price=item['price'],quantity=item['quantity'])
            request.session['order_id']=order.id
            return redirect('payment:create_checkout_session')
    else:
        form=OrderCreateForm()
    return render(request,'orders/create.html',{'cart':cart,'form':form})
