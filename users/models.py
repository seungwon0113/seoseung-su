from django.contrib.auth.models import AbstractUser
from django.db import models

from config.basemodel import BaseModel


# Create your models here.
class User(AbstractUser, BaseModel):
    class Gender(models.TextChoices):
        MALE = 'Male', "남자"
        FEMALE = "Female", "여자"
    class Role(models.TextChoices):
        ADMIN = 'admin', "관리자"
        CONSUMER = 'consumer', '소비자'
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CONSUMER)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=None, null=True)
    phone_number = models.CharField(max_length=13, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    personal_info_consent = models.BooleanField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

class PermissionAdmin(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'admin_permissions'

class PermissionConsumer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'consumer_permissions'