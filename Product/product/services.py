from .models import Product
from .serializers import ProductSerializer
from mongoengine.errors import DoesNotExist 
from .repositories import ProductRepository



class ProductService:
    def list_products(self):             # Returns all products
        return ProductRepository().find_all()
    
    def get_product_by_id(self,product_id):     # Returns a product by id
        try:
            product_instance = ProductRepository().find_by_id(product_id)
            if product_instance:
                return {"success":True,"data":ProductSerializer(product_instance).data}
            else: 
                return {"error":"Product not found"}
        except DoesNotExist:
            return {"error": "Product not found"}
    
    def get_product_by_name(self,product_name):     # Returns a product by name
        try:
            product_instance = ProductRepository().find_by_name(product_name)
            if product_instance:
                return {"success":True,"data":ProductSerializer(product_instance).data}
            else: 
                return {"error":"Product not found"}
        except DoesNotExist:
            return {"error": "Product not found"}

    def create_product(self,product):       # Creates a product
        serializer=ProductSerializer(data=product)
        if serializer.is_valid():
            ProductRepository().create_product(serializer)
            return  {"success": True,"data": serializer.data}
        else:
            return {"success": False,"error": serializer.errors}
        
    def update_product(self,product):       # Updates a product     
        if int(product['quantity'])<0:
            raise ValueError("Quantity cannot be negative")
        existing_product=ProductRepository().find_by_name(product['name'])
        if not existing_product:
            return {"error":"Product not found"}
        updated_product=ProductRepository().update_product(product['name'],product)
        return {"success":True,"data":updated_product}
        
    def delete_product(self,product):       # Deletes a product
        ProductRepository().delete_product(product['name'])
        return "Product deleted successfully"