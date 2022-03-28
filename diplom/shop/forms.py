from django import forms


class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    address = forms.CharField(max_length=250)
    postal_code = forms.CharField(max_length=20)


class CommentForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    body = forms.CharField()
