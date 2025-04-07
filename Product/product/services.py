from .serializers import ProductSerializer, ProductCategorySerializer
from mongoengine.errors import DoesNotExist 
from .repositories import ProductRepository, ProductCategoryRepository

product_category_repository=ProductCategoryRepository()
product_repository=ProductRepository()

class ProductService:
    def list_products(self):             # Returns all products
        return ProductRepository().find_all()
    
    def get_product_by_id(self,product_id):     # Returns a product by id
        try:
            product_instance = ProductRepository().find_by_id(product_id)
            if product_instance:
                return {"success":True,"data":ProductSerializer(product_instance).data}
            else: 
                return {"success":False,"error":"Product not found"}
        except DoesNotExist:
            return {"success":False,"error": "Product not found"}
    
    def get_product_by_name(self,product_name):     # Returns a product by name
        try:
            product_instance = ProductRepository().find_by_name(product_name)
            if product_instance:
                return {"success":True,"data":ProductSerializer(product_instance).data}
            else: 
                return {"success":False,"error":"Product not found"}
        except DoesNotExist:
            return {"success":False,"error": "Product not found"}

    def create_product(self,product):       # Creates a product
        category_title=product['category']
        try:
            existing_category=ProductCategoryRepository().find_by_name(category_title)
            if existing_category['success']==False:
                return {"success":False,"error":"Category not found"}
        except DoesNotExist:
            return {"success":False,"error":"Category not found"}
        
        if int(product['quantity'])<0:
            return {"success":False,"error":"Quantity cannot be negative"}
        product['category']=existing_category['data']['id']
        serializer=ProductSerializer(data=product)
        if serializer.is_valid():
            ProductRepository().create_product(serializer)
            return  {"success": True,"data": serializer.data}
        else:
            return {"success": False,"error": serializer.errors}
        
    def update_product(self,product):       # Updates a product     
        if int(product['quantity'])<0:
            return {"success":False,"error":"Quantity cannot be negative"}
        existing_product=ProductRepository().find_by_name(product['name'])
        if not existing_product:
            return {"success":False,"error":"Product not found"}
        existing_category=ProductCategoryRepository().find_by_name(product['category'])
        if existing_category['success']==False:
            return {"success":False,"error":"Category not found"}
        product['category']=existing_category['data']['id']
        updated_product=ProductRepository().update_product(product['name'],product)
        return {"success":True,"data":updated_product}
        
    def delete_product(self,product_name):       # Deletes a product
        try:
            ProductRepository().delete_product(product_name)
            return {"success":True,"message":"Product deleted successfully"}
        except Exception as e:
            return {"success":False,"error":str(e)}
    
# Create, Read, Update, Delete operations for ProductCategory
class ProductCategoryService:
    def create_product_category(self,category):
        serializer=ProductCategorySerializer(data=category)
        if serializer.is_valid():
            return product_category_repository.create_product_category(serializer)
        else:
            return {"success":False,"error":serializer.errors}
        
    def list_product_categories(self):
        return product_category_repository.find_all_categories()
    
    def get_products_by_category(self,category_title):
        return product_category_repository.find_products_by_category(category_title)

    def get_category_by_name(self,category_name):
        return product_category_repository.find_by_name(category_name)

        
    def update_category(self,category):
        return product_category_repository.update_category(category)
        
    
    def delete_product_category(self,category_title):
        return product_category_repository.delete_product_category(category_title)
    

