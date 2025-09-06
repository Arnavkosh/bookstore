from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Book
from .cart import Cart

@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    qty = int(request.POST.get('quantity', 1))
    cart.add(book=book, quantity=qty)

    if request.POST.get("buy_now"):  # agar Buy Now button dabaya
        return redirect("orders:order_create")  # seedha checkout pe bhej de
    
    return redirect("cart:cart_detail")

def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect("cart:cart_detail")

def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart": cart})
