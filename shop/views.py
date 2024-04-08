from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from cart.forms import CartAddProductForm
from shop.models import Customer, Order, Ticker, Product


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'
    model = Ticker
    context_object_name = "list_of_tickers"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')
        is_trading_filter = self.request.GET.get('isTrading')
        sort_filter = self.request.GET.get('sort')

        # Apply filters based on user selection
        if is_trading_filter:
            queryset = queryset.filter(is_trading=is_trading_filter)
        if sort_filter:
            # Example sorting logic fr volume:
            if sort_filter == "volume_asc":
                queryset = queryset.order_by('volume')
            elif sort_filter == "volume_desc":
                queryset = queryset.order_by('-volume')
            pass

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(full_name__icontains=search_query))

        return queryset




def ticker_details(request, slug):
    ticker = get_object_or_404(Ticker, slug=slug)
    options = ticker.tickers.all()
    cart_product_form = CartAddProductForm()
    context = {'ticker': ticker, 'options': options, 'cart_product_form': cart_product_form}
    return render(request, 'shop/tickers/details.html', context)


def product_details(request, slug):
    option = get_object_or_404(Product, slug=slug)
    cart_product_form = CartAddProductForm()
    context = {'options': option, 'cart_product_form': cart_product_form}
    return render(request, 'shop/products/product.html', context)


class CustomersListView(ListView):
    template_name = "customer.html"
    model = Customer
    context_object_name = "list_of_all_customers"


#class OrdersListView(ListView):
#    template_name = "orders.html"
#    model = Order
#    context_object_name = "list_of_all_orders"


#class SearchView(ListView):
#    template_name = "search.html"
#    model = Order
#    context_object_name = "list_of_all_orders"

#    def get_queryset(self):
#        query = self.request.GET.get('q')
#        return Order.objects.filter(
#            Q(customer__first_name__icontains=query) | Q(customer__last_name__icontains=query)
#        ).order_by('order_date').reverse()
