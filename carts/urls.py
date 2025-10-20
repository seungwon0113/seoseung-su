from django.urls import path

from carts.views.cart_create import CartCreateView
from carts.views.cart_delete import CartDeleteView
from carts.views.cart_detail_or_list import CartDetailView
from carts.views.cart_update import CartUpdateView

urlpatterns = [
    path('create/', CartCreateView.as_view(), name='cart-create'),
    path('', CartDetailView.as_view(), name='cart-detail'),
    path('delete/<int:cart_id>/', CartDeleteView.as_view(), name='cart-delete'),
    path('update/<int:cart_id>/', CartUpdateView.as_view(), name='cart-update'),
]