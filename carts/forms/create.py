from typing import Any, cast

from django import forms

from products.models import Product


class CartCreateForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1, initial=1)
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({
            'class': 'form-control',
            'min': '1'
        })
    
    def clean_product_id(self) -> Product:
        product_id = cast(int, self.cleaned_data.get('product_id'))
        try:
            product = Product.objects.get(id=product_id)
            return product
        except Product.DoesNotExist:
            raise forms.ValidationError('존재하지 않는 상품입니다.')
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = cast(dict[str, Any], super().clean())

        product = cast(Product | None, cleaned_data.get('product_id'))
        quantity = cast(int | None, cleaned_data.get('quantity'))

        if product and quantity:
            if quantity > product.stock:
                self.add_error('quantity', '재고가 부족합니다.')

        return cleaned_data