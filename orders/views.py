from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from accounts.views import user_profile
from .forms import OrderCreateForm
from .models import OrderItem
from cart.cart import Cart


# Create your views here.
@login_required
def order_create(request):
    cart = Cart(request)
    if cart.__len__() < 1:
        return user_profile(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)  # Don't save immediately
            order.user = request.user  # Assign the current user to the order
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            message = f'''Your order has been successfully created \n \n Order Details \n
        - Order ID: {order.id}
        - Date: {order.created}
        - Address: {order.city}
        - Total: {order.address}, {order.city}

        Thank you for your order
      '''
            send_mail(f'Order from AI options on {order.created}', message, None, [order.email])
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        user = request.user
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        form = OrderCreateForm(initial=initial_data)
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})