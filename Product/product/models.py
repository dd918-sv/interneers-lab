from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=100, null=False,unique=True)
    description=models.TextField(null=True)
    category=models.CharField(max_length=100,null=True)
    price=models.FloatField(MinValueValidator(1.0), null=False)
    brand=models.CharField(max_length=100,null=True)
    quantity=models.IntegerField(MinValueValidator(0),null=True)
    
    def __str__(self):
        return self.name
    
