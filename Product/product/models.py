from mongoengine import Document,StringField,FloatField, IntField, DateTimeField,ReferenceField
from datetime import datetime

# Create your models here.
class ProductCategory(Document):
    title=StringField(max_length=100,null=False,unique=True)
    description=StringField(null=True)
    meta={'collection':'product_categories',
          'indexes':['title']}

class Product(Document):
    name=StringField(max_length=100, null=False,unique=True)
    description=StringField(null=True)
    category=ReferenceField(ProductCategory,null=False,reverse_delete_rule=2)
    # category=StringField(max_length=100,null=True)
    price=FloatField(min_value=1.0, null=False)
    brand=StringField(max_length=100,null=True)
    quantity=IntField(min_value=0,null=True)
    created_at=DateTimeField(default=datetime.now)
    updated_at=DateTimeField(default=datetime.now)
    meta={'collection':'products',
          'indexes':['name','category']
          }
    
    
    def __str__(self):
        return self.name
    def save(self,*args,**kwargs):
        self.updated_at=datetime.now()
        return super(Product,self).save(*args,**kwargs)




