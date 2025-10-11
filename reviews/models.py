from django.core.validators import MaxValueValidator, MinValueValidator
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
    rating = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    images = models.ManyToManyField(ReviewImage, blank=True, related_name='reviews', db_table='review_image_cdt')
    is_published = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'reviews'
    
    def get_star_display(self) -> str:
        return '★' * self.rating + '☆' * (5 - self.rating)
    
    def get_masked_username(self) -> str:
        username = self.user.username
        if len(username) <= 1:
            return username
        return username[0] + '*' * (len(username) - 1)


class ReviewComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'review_comments'