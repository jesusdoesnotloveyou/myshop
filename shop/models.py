# Create your models here.
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q, Count, Avg
from django.urls import reverse


class Customer(models.Model):
    customer_id = models.AutoField("ID", primary_key=True)
    email = models.EmailField("E-mail", max_length=128)
    first_name = models.CharField("First Name", max_length=128)
    last_name = models.CharField("Last Name", max_length=128)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Order(models.Model):
    order_id = models.AutoField("ID", primary_key=True)
    product = models.CharField("Product", max_length=128)
    order_date = models.DateField("Order Date")
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return '%s %s' % (self.order_id, self.product)


class Ticker(models.Model):
    name = models.CharField(max_length=10, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    full_name = models.CharField(max_length=100, db_index=True, unique=True)
    last_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    change = models.DecimalField(max_digits=10, decimal_places=2)
    percent_change = models.DecimalField(max_digits=10, decimal_places=2)
    market_cap = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    isTrading = models.BooleanField(blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ticker'
        verbose_name_plural = 'Tickers'

    def __str__(self):
        return self.name


class OptionType(models.TextChoices):
    CALL = 'Call'
    PUT = 'Put'


class Product(models.Model):
    option_type = models.CharField(max_length=4, choices=OptionType.choices)
    category = models.ForeignKey(Ticker, related_name='tickers', on_delete=models.RESTRICT)
    name = models.CharField(max_length=20, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    ask = models.DecimalField(max_digits=10, decimal_places=2)
    strike = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.PositiveIntegerField()
    expiration_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])

    def average_review(self):
        review = Review.objects.filter(product=self).aggregate(avarage=Avg('rate'))
        avg = 0
        if review["average"] is not None:
            avg = float(review["average"])
        return avg

    def count_review(self):
        reviews = Review.objects.filter(product=self).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        constraints = [
            CheckConstraint(
                check=Q(option_type__in=OptionType.values),
                name="valid_option_type")
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE, null=True, blank=True)
    comment = models.TextField(max_length=250, null=True, blank=True)
    rate = models.IntegerField(default=0, validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)