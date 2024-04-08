from django import forms
from .models import Order
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']


class PaymentForm(forms.Form):
    card_holder = forms.CharField(label='Card Holder')
    cc_number = CardNumberField(label='Card Number', widget=forms.TextInput(attrs={'placeholder': '0000 0000 0000 0000'}))
    cc_expiry = CardExpiryField(label='Expiration Date')
    cc_code = SecurityCodeField(label='CVV/CVC')