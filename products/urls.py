from django.urls import path

from products.views.admin.create_update import ProductCreateView, ProductUpdateView
from products.views.admin.delete_image import DeleteProductImageView
from products.views.admin.detail_or_list import ProductListView
from products.views.products_detail import ProductsDetailView

urlpatterns = [
    path("<str:product_name>", ProductsDetailView.as_view(), name="products-detail"),
    
    # 어드민 URL
    path("admin_page/", ProductListView.as_view(), name="product-list"),
    path("admin/create/", ProductCreateView.as_view(), name="product-create"),
    path("admin/<int:pk>/update/", ProductUpdateView.as_view(), name="product-update"),
    path("admin/image/<int:image_id>/delete/", DeleteProductImageView.as_view(), name="product-delete-image"),
]