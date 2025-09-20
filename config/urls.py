"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import include, path

from config import settings
from users import urls as users_urls


def home(request: HttpRequest) -> HttpResponse:
    from products.models import Product
    # 판매 중인 상품 중 최신 4개를 가져옴
    products = Product.objects.filter(is_live=True, is_sold=False).order_by('-created_at')[:4]
    context = {'products': products}
    return render(request, 'home.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path("users/", include(users_urls), name='users'),
    path("products/", include("products.urls"), name='products'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
