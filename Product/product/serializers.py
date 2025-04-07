from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Product, ProductCategory

class ProductSerializer(DocumentSerializer):
    class Meta:
        model=Product
        fields='__all__'
        read_only_fields=('created_at','updated_at')
        ordering=['-created_at']
        verbose_name='Product'
        verbose_name_plural='Products'

class ProductCategorySerializer(DocumentSerializer):
    class Meta:
        model=ProductCategory
        fields='__all__'