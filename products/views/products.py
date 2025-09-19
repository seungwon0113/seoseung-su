from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from products.models import Product


class ProductsDetailView(View):
    def get(self, request: HttpRequest, product_name: str) -> HttpResponse:
        products = Product.objects.get(name=product_name)
        context = {"products": products}
        return render(request, "products/detail.html", context)