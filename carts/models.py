from django.core.validators import MinValueValidator
from django.db import models

from config.basemodel import BaseModel
from products.models import Product
from users.models import User


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        db_table = 'carts'