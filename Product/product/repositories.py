from .models import Product,ProductCategory
from .serializers import ProductSerializer,ProductCategorySerializer

class ProductRepository:
    def find_all(self):
        return Product.objects.all()
    
    def find_by_id(self,product_id):
        return Product.objects.get(id=product_id)
    
    def find_by_name(self,product_name):
        return Product.objects.get(name=product_name)
    
    def find_by_categoryID(self,categoryID):
        try:
            category_instance=ProductCategory.objects.get(id=categoryID)
        except ProductCategory.DoesNotExist:
            return {"success":False,"error":"Category not found"}
        return Product.objects.filter(category=categoryID)

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

class ProductCategoryRepository:
    def find_all_categories(self):
        try:
            return ProductCategory.objects.all()
        except Exception as e:  
            return {"success":False,"error": str(e)}

    def find_products_by_category(self,category_title):
        try:
            category_instance = ProductCategory.objects.get(title=category_title)
            if category_instance:
                category_id=category_instance['id']
                print(category_id)
                return Product.objects.filter(category=category_id)
            else:
                return {"success":False,"error":"Category not found"}
        except Exception as e:
            return {"success":False,"error": str(e)}
            
    def find_by_name(self,category_name):
        try:
            category_instance= ProductCategory.objects.get(title=category_name)
            if category_instance:
                serializer=ProductCategorySerializer(category_instance)
                return {"success":True,"data":serializer.data}
            else:
                return {"success":False,"error":"Category not found"}
        except Exception as e:
            return {"success":False,"error": str(e)}
        
    def find_by_ID(self,category_id):
        try:
            category_instance= ProductCategory.objects.get(id=category_id)
            if category_instance:
                serializer=ProductCategorySerializer(category_instance)
                return {"success":True,"data":serializer.data}
            else:
                return {"success":False,"error":"Category not found"}
        except Exception as e:
            return {"success":False,"error": str(e)}
    
    def create_product_category(self,serializer):
        try:
            serializer.save()
            return {"success":True,"data":serializer.data}
        except Exception as e:
            return {"success":False,"error": str(e)}
        
    def update_category(self,category):
        try:
            category_instance=ProductCategory.objects.get(title=category['title'])
            if not category_instance:
                return {"success":False,"error":"Category not found"}
            
            serializer=ProductCategorySerializer(category_instance,data=category,partial=True)
            if serializer.is_valid():
                serializer.save()
                return {"success":True,"data":serializer.data}
            else:
                return {"success":False,"error":serializer.errors}
        except Exception as e:
            return {"success":False,"error": str(e)}
        
    def delete_product_category(self,category_title):
        try:
            category_instance=ProductCategory.objects.get(title=category_title)
            if category_instance:
                category_instance.delete()
                return {"success":True,"message":"Category deleted successfully"}
            else:
                return {"success":False,"error":"Category not found"}
        except Exception as e:
            return {"success":False,"error": str(e)}

        


    

