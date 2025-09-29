import os
from typing import cast

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from products.forms.product_form import ProductForm, ProductImageForm
from products.models import Product, ProductImage
from users.models import User
from users.utils.permission import AdminPermission


def ensure_media_directory() -> None:
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if media_root:
        # products/images 디렉토리 생성
        products_images_dir = os.path.join(media_root, 'products', 'images')
        os.makedirs(products_images_dir, mode=0o755, exist_ok=True)


class ProductCreateView(AdminPermission, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = ProductForm()
        image_form = ProductImageForm()
        context = {
            'form': form,
            'image_form': image_form,
            'title': '상품 등록'
        }
        return render(request, 'products/admin/product_form.html', context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ProductForm(request.POST)
        image_form = ProductImageForm(request.POST, request.FILES)
        
        if form.is_valid() and image_form.is_valid():
            product = form.save(commit=False)
            product.user = cast(User, request.user)
            product.save()
            
            # 이미지 처리 (이미지가 있는 경우에만)
            images = request.FILES.getlist('image')
            if images:
                # media 디렉토리 확인 및 생성
                ensure_media_directory()
                
                for image in images:
                    product_image = ProductImage.objects.create(image=image)
                    product.image.add(product_image)
            
            return redirect('product-list')
        
        context = {
            'form': form,
            'image_form': image_form,
            'title': '상품 등록'
        }
        return render(request, 'products/admin/product_form.html', context)


class ProductUpdateView(AdminPermission, View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        image_form = ProductImageForm()
        context = {
            'form': form,
            'image_form': image_form,
            'product': product,
            'title': '상품 수정'
        }
        return render(request, 'products/admin/product_form.html', context)

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, instance=product)
        image_form = ProductImageForm(request.POST, request.FILES)
        
        if form.is_valid() and image_form.is_valid():
            form.save()
            
            # 새 이미지 추가 (이미지가 있는 경우에만)
            images = request.FILES.getlist('image')
            if images:
                # media 디렉토리 확인 및 생성
                ensure_media_directory()
                
                for image in images:
                    product_image = ProductImage.objects.create(image=image)
                    product.image.add(product_image)
            
            return redirect('product-list')
        
        context = {
            'form': form,
            'image_form': image_form,
            'product': product,
            'title': '상품 수정'
        }
        return render(request, 'products/admin/product_form.html', context)


