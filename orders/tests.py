from django.contrib.auth.models import User
from django.test import TestCase

from orders.models import Order, OrderItem
from shop.models import Product


# Create your tests here.


class OrderModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword'
        )
        self.order = Order.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            address='Test Address',
            postal_code='12345',
            city='Test City',
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=10.00,
            available=True,
        )

    def test_order_creation(self):
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.first_name, 'John')
        self.assertEqual(order.last_name, 'Doe')
        self.assertEqual(order.email, 'johndoe@example.com')
        self.assertEqual(order.address, 'Test Address')
        self.assertEqual(order.postal_code, '12345')
        self.assertEqual(order.city, 'Test City')
        self.assertFalse(order.paid)

    def test_order_total_cost(self):
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
            quantity=2,
        )
        self.assertEqual(self.order.get_total_cost(), 20.00)

    def test_order_item_creation(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
            quantity=3,
        )
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.price, self.product.price)
        self.assertEqual(order_item.quantity, 3)

    def test_order_item_cost(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
            quantity=4,
        )
        self.assertEqual(order_item.get_cost(), 40.00)