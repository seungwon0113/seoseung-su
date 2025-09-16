from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'Male', "남자"
        FEMALE = "Female", "여자"
    gender = models.CharField(max_length=10, choices=Gender.choices, default=None, null=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'