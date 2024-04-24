from django import forms

from shop.models import Review


# class ReviewForm(forms.Form):
#     review = forms.CharField(widget=forms.Textarea, label='')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rate']
        widgets = {
            "comment": forms.Textarea(),
            "rate": forms.HiddenInput()
        }
        labels = {
            "comment": "What do you think about this product",
        }
