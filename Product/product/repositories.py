from .models import Product
from .serializers import ProductSerializer

class ProductRepository:
    def find_all(self):
        return Product.objects.all()
    
    def find_by_id(self,product_id):
        return Product.objects.get(id=product_id)
    
    def find_by_name(self,product_name):
        return Product.objects.get(name=product_name)

    def create_product(self,serializer):
        serializer.save()

    def update_product(self,product_name,data):
        product=Product.objects.get(name=product_name)
        serializer=ProductSerializer(product,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            return serializer.errors

    def delete_product(self,product_name):
        product=Product.objects.get(name=product_name)
        product.delete()

    

