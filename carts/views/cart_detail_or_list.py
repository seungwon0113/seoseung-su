from decimal import Decimal
from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from carts.models import Cart
from users.models import User


class CartDetailView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        user = cast(User, request.user)
        cart_items = Cart.objects.filter(user=user).select_related('product')
        
        # 총 가격 계산
        total_price = Decimal("0")
        for item in cart_items:
            if item.product.sale_price:
                item_price = item.product.price  # 할인가
            else:
                item_price = item.product.price
            total_price += item_price * item.quantity
        
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        return render(request, 'carts/cart_detail.html', context)
