from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from carts.forms.update import CartUpdateForm
from carts.models import Cart


class CartUpdateView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, cart_id: int) -> HttpResponse:
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
        form = CartUpdateForm(request.POST)
        
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            if quantity <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()

            return redirect('cart-detail')
        
        return redirect('cart-detail')
