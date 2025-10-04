from django.db import models

from config.basemodel import BaseModel
from config.utils.image_path import image_upload_path
from products.models import Product
from users.models import User


def review_image_upload_path(instance: 'ReviewImage', filename: str) -> str:
    return image_upload_path('reviews', filename)


class ReviewImage(BaseModel):
    image = models.ImageField(upload_to=review_image_upload_path)
    
    class Meta:
        db_table = 'reviews_image'


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField(max_length=1000)
    rating = models.PositiveIntegerField(default=5)
    images = models.ForeignKey(ReviewImage, blank=True, on_delete=models.CASCADE, related_name='reviews_images')
    is_published = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'reviews'

class ReviewComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'review_comments'