from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View

from products.models import Product


class ProductsDetailView(View):
    def get(self, request: HttpRequest, product_name: str) -> HttpResponse:
        products = get_object_or_404(Product, name=product_name)
        context = {"products": products}
        return render(request, "products/detail.html", context)