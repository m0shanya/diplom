from django import forms
from django.core.exceptions import ValidationError


class ProductFiltersForm(forms.Form):
    ORDER_BY_CHOICES = (
        ("cost_asc", "Cost Asc"),
        ("cost_desc", "Cost Desc"),
        ("max_price", "Max Cost"),
    )
    cost__gt = forms.IntegerField(min_value=0, label="Cost Min", required=False)
    cost__lt = forms.IntegerField(min_value=0, label="Cost Max", required=False)
    order_by = forms.ChoiceField(choices=ORDER_BY_CHOICES, required=False)

    def clean(self):
        cleaned_data = super().clean()
        cost__gt = cleaned_data.get("cost__gt")
        cost__lt = cleaned_data.get("cost__lt")
        if cost__gt and cost__lt and cost__gt > cost__lt:
            raise ValidationError("Min price can't be greater than Max price")


class OrderForm(forms.Form):
    DELIVERY_CHOICES = [
        ('PU', 'Pickup'),
        ('HD', 'Home delivery')
    ]
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    address = forms.CharField(max_length=250)
    postal_code = forms.CharField(max_length=20)
    delivery = forms.TypedChoiceField(choices=DELIVERY_CHOICES)


class CommentForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    body = forms.CharField(widget=forms.Textarea)
