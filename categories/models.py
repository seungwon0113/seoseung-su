from django.db import models

from config.basemodel import BaseModel


# Create your models here.
class Category(BaseModel):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'categories'
