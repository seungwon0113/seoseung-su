from typing import Any

from django import forms


class CartUpdateForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({
            'class': 'quantity-input',
            'min': '1'
        })
    
    def clean_quantity(self) -> int:
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity < 1:
            raise forms.ValidationError('수량은 1개 이상이어야 합니다.')
        return int(quantity)
