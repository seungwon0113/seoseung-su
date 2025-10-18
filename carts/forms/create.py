from django import forms

from carts.models import Cart


class CartCreateForm(forms.Form):
    product = forms.CharField()
    quantity = forms.IntegerField()

    class Meta:
        model = Cart
        fields = ['product', 'quantity']