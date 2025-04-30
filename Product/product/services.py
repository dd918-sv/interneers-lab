from .serializers import ProductSerializer, ProductCategorySerializer
from mongoengine.errors import DoesNotExist 
from .repositories import ProductRepository, ProductCategoryRepository

product_category_repository=ProductCategoryRepository()
product_repository=ProductRepository()

class ProductService:
    def __init__(self,repository=None):
        self.repository=repository or product_repository

    def list_products(self):             # Returns all products
        return self.repository.find_all()
    
    def get_product_by_id(self,product_id):     # Returns a product by id
        try:
            product_instance = self.repository.find_by_id(product_id)
            if product_instance:
                return {"success":True,"data":ProductSerializer(product_instance).data}
            else: 
                return {"success":False,"error":"Product not found"}
        except DoesNotExist:
            return {"success":False,"error": "Product not found"}
    
    def get_product_by_name(self,product_name):     # Returns a product by name
        try:
            product_instance = self.repository.find_by_name(product_name)
            if product_instance:
                return {"success":True,"data":ProductSerializer(product_instance).data}
            else: 
                return {"success":False,"error":"Product not found"}
        except DoesNotExist:
            return {"success":False,"error": "Product not found"}
    
    def get_products_by_categoryID(self,category_id):
        try:
            product_instance = self.repository.find_by_categoryID(category_id)
            if product_instance:
                return {"success":True,"data":product_instance}
            else: 
                return {"success":False,"error":"Product not found"}
        except DoesNotExist:
            return {"success":False,"error": "Products not found"}

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
            self.repository.create_product(serializer)
            return  {"success": True,"data": serializer.data}
        else:
            return {"success": False,"error": serializer.errors}
        
    def update_product(self,product):       # Updates a product     
        if 'quantity' in product and int(product['quantity'])<0:
            return {"success":False,"error":"Quantity cannot be negative"}
        existing_product=self.repository.find_by_name(product['name'])
        if not existing_product:
            return {"success":False,"error":"Product not found"}
        existing_category=ProductCategoryRepository().find_by_name(product['category'])
        if existing_category['success']==False:
            return {"success":False,"error":"Category not found"}
        product['category']=existing_category['data']['id']
        updated_product=self.repository.update_product(product['name'],product)
        return {"success":True,"data":updated_product}
        
    def delete_product(self,product_name):       # Deletes a product
        try:
            self.repository.delete_product(product_name)
            return {"success":True,"message":"Product deleted successfully"}
        except Exception as e:
            return {"success":False,"error":str(e)}
    
# Create, Read, Update, Delete operations for ProductCategory
class ProductCategoryService:
    def __init__(self,repository=None):
        if repository is None:
            self.repository=product_category_repository
        else: 
            self.repository=repository

    def create_product_category(self,category):
        serializer=ProductCategorySerializer(data=category)
        if serializer.is_valid():
            self.repository.create_product_category(serializer)
            return {"success":True,"data":serializer.data}
        else:
            return {"success":False,"error":serializer.errors}
        
    def list_product_categories(self):
        return self.repository.find_all_categories()
    
    def get_products_by_category(self,category_title):
        return self.repository.find_products_by_category(category_title)

    def get_category_by_name(self,category_name):
        return self.repository.find_by_name(category_name)
    
    def get_category_by_id(self,category_id):
        return self.repository.find_by_ID(category_id)

        
    def update_category(self,category):
        return self.repository.update_category(category)
        
    
    def delete_product_category(self,category_title):
        return self.repository.delete_product_category(category_title)
    

