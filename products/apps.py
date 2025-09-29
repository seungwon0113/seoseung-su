import os

from django.apps import AppConfig
from django.conf import settings


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    
    def ready(self) -> None:
        try:
            if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
                products_images_dir = os.path.join(settings.MEDIA_ROOT, 'products', 'images')
                os.makedirs(products_images_dir, mode=0o755, exist_ok=True)
        except (PermissionError, OSError):
            # 권한 오류나 기타 OS 오류는 무시 (런타임에서 처리)
            pass