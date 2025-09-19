from django.urls import path

from products.views.products import ProductsDetailView

urlpatterns = [
    path("<str:product_name>", ProductsDetailView.as_view(), name="products-detail"),
]