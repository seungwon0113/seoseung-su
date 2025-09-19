
from django.db import models

from config.basemodel import BaseModel
from users.models import User


class ProductImage(BaseModel):
    image = models.ImageField()
    class Meta:
        db_table = 'products_image'

# Create your models here.
class Product(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ManyToManyField(ProductImage, blank=True, db_table='product_image_cdt')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    is_live = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    class Meta:
        db_table = 'products'

class WishList(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    class Meta:
        db_table = 'wish_list'