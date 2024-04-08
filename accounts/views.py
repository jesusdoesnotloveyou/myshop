# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST

from orders.forms import PaymentForm
from shop.forms import ReviewForm
from shop.models import Order
from shop.models import Review, Product


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


@login_required
def user_profile(request):
    current_user = request.user
    orders = Order.objects.filter(user=current_user)
    card_form = PaymentForm()
    review_form = ReviewForm()
    context = {
        'user': current_user,
        'orders': orders,
        'form': card_form,
        'review_form': review_form,
    }
    return render(request, 'accounts/profile.html', context)


@require_POST
def complete_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.paid = True
    order.save()
    message = f'''Your order has been successfully paid \n \n Order Details \n
            - Order ID: {order.id}
            - Date: {order.created}
            - Address: {order.address} {order.city}
            - Total: {order.get_total_cost()}

    Thank you for your Payment
          '''
    send_mail(f'Payment from AI options', message, None, [order.email])
    return redirect('profile')


@require_POST
def add_review(request, product_id):
    print(request)
    print(request.POST)
    product = get_object_or_404(Product, id=product_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)  # Don't save immediately
        review.user = request.user  # Assign the current user to the order
        review.product = product  # Assign the current user to the order
        review.save()
    return redirect('profile')