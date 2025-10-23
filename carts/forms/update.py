from typing import Any

from django import forms


class CartUpdateForm(forms.Form):
    quantity = forms.IntegerField(initial=1)
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({
            'class': 'quantity-input',
            'min': '1'
        })

    def clean_quantity(self) -> int:
        raw_quantity = self.cleaned_data.get('quantity')
        if raw_quantity is None or raw_quantity < 1:
            raise forms.ValidationError('수량은 1개 이상이어야 합니다.')

        quantity: int = raw_quantity
        return quantity
