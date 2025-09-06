from django.shortcuts import render, redirect
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('book_list')
    return render(request, 'orders/create.html', {'cart': cart})
