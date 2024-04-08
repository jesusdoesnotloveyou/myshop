# Create your tests here.
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from orders.forms import PaymentForm
from orders.models import Order


class SignUpViewTestCase(TestCase):
    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword'
        )
        self.order = Order.objects.create(
            user=self.user, address='Test Address', city='Test City'
        )

    def test_user_profile_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertIn('user', response.context)
        self.assertIn('orders', response.context)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], PaymentForm)

    def test_user_profile_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {'card_number': '1234567890', 'expiry_date': '12/25', 'cvv': '123'}
        response = self.client.post(reverse('profile'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')


class CompletePaymentViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword'
        )
        self.order = Order.objects.create(
            user=self.user, address='Test Address', city='Test City'
        )

    def test_complete_payment_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('complete_payment', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertTrue(self.order.paid)