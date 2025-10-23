import os
import uuid
from typing import Literal

APPS_CATEGORY = {
    'products': 'products',
    'reviews': 'reviews',
}

def image_upload_path(image_category: Literal['products', 'reviews'], filename: str) -> str:
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(APPS_CATEGORY[image_category], 'images', filename)