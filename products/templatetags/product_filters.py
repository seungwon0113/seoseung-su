from typing import Union

from django import template

register = template.Library()

@register.filter
def discount_rate(price: Union[int, float], sale_price: Union[int, float]) -> int:
    if not price or not sale_price or price <= 0:
        return 0
    
    discount = ((price - sale_price) / price) * 100
    return round(discount)
