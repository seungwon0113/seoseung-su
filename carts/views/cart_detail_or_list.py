from decimal import Decimal
from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import DecimalField, F, Sum
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
        total_price = cart_items.aggregate(
            total=Sum(F('quantity') * F('product__price'), output_field=DecimalField())
        )['total'] or Decimal('0')
        
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        return render(request, 'carts/cart_detail.html', context)
