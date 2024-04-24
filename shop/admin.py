from shop.models import Customer, Order, Review

from django.contrib import admin
from .models import Ticker, Product

admin.site.register(Customer)
admin.site.register(Order)


class TickerAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'full_name', 'last_price', 'image', 'volume', 'change', 'percent_change',
                    'market_cap', 'description', 'isTrading']
    list_editable = ['full_name', 'last_price', 'volume', 'change', 'image', 'percent_change', 'market_cap',
                     'description', 'isTrading']
    list_filter = ['isTrading']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Ticker, TickerAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'strike', 'category', 'bid', 'ask', 'volume',
                    'option_type', 'expiration_date', 'created', 'updated']
    list_filter = ['option_type', 'created', 'updated']
    list_editable = ['expiration_date', 'name', 'strike', 'category', 'bid', 'ask', 'volume',
                     'option_type', ]
    list_display_links = None
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'rate', 'product', 'created_at']
    list_filter = ['comment', 'rate', 'user', 'product']
    list_editable = ['comment', 'rate', 'user', 'product']
    list_display_links = None


admin.site.register(Review, ReviewAdmin)
