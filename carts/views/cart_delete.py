from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from carts.models import Cart


class CartDeleteView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, cart_id: int) -> HttpResponse:
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
        cart_item.delete()
        return redirect('cart-detail')
