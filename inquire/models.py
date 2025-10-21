from django.db import models

from config.basemodel import BaseModel
from users.models import User


class Inquire(BaseModel):
    class Item(models.TextChoices):
        PRODUCT = 'product', '상품 불량/교환 문의'
        DELIVERY = 'delivery', '배송 문의'
        PAYMENT = 'payment', '결제 문의'
        WEBSITE = 'website', '웹사이트 오류 문의'
        ETC = 'etc', '기타 문의'
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    item = models.CharField(choices=Item.choices, max_length=20, default=Item.ETC)

    class Meta:
        db_table = 'inquire'

