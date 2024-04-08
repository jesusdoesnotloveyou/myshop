from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


# Create your views here.


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        # так как используется структура словаря, то добавление уже имеющегося продукта в корзину увеличит его количество
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_update_quantity(request, product_id, action):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = cart.cart.get(str(product_id), {}).get('quantity', 0)
    if action == 'increase':
        cart.update_quantity(product=product, quantity=quantity + 1)
    elif action == 'decrease':
        if quantity > 1:
            cart.update_quantity(product=product, quantity=quantity - 1)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})