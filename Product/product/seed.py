from .services import ProductService, ProductCategoryService
import logging
from .models import Product, ProductCategory

logger = logging.getLogger(__name__)

def clear_all_data():
    Product.objects.all().delete()
    ProductCategory.objects.all().delete()
    logger.info("Cleared all existing product and category data")

def seed_categories(categories=None):
    if categories is None:
        categories = [
            {"title": "Category 1", "description": "Description for Category 1"},
            {"title": "Category 2", "description": "Description for Category 2"},
            {"title": "Category 3", "description": "Description for Category 3"},
            {"title": "Category 4", "description": "Description for Category 4"},
            {"title": "Category 5", "description": "Description for Category 5"}
        ]
    
    service = ProductCategoryService()
    created = 0
    
    for category in categories:
        response = service.create_product_category(category)
        if response['success']:
            logger.info(f"Category '{category['title']}' created")
            created += 1
        else:
            logger.warning(f"Category '{category['title']}' creation failed: {response.get('error', 'Unknown error')}")
    
    return created

def seed_products(products=None):
    if products is None:
        products = [
            {
                "name": "Product 1", "description": "Description for Product 1",
                "category": "Category 1", "price": 10.0, "brand": "Brand A", "quantity": 100
            },
            {
                "name": "Product 2", "description": "Description for Product 2",
                "category": "Category 1", "price": 20.0, "brand": "Brand A", "quantity": 200
            },
            {
                "name": "Product 3", "description": "Description for Product 3",
                "category": "Category 1", "price": 30.0, "brand": "Brand B", "quantity": 300
            },
            {
                "name": "Product 4", "description": "Description for Product 4",
                "category": "Category 2", "price": 40.0, "brand": "Brand B", "quantity": 400
            },
            {
                "name": "Product 5", "description": "Description for Product 5",
                "category": "Category 2", "price": 50.0, "brand": "Brand C", "quantity": 500
            },
            {
                "name": "Product 6", "description": "Description for Product 6",
                "category": "Category 2", "price": 60.0, "brand": "Brand C", "quantity": 600
            }
        ]
    
    service = ProductService()
    created = 0
    
    for product in products:
        response = service.create_product(product)
        if response['success']:
            logger.info(f"Product '{product['name']}' created")
            created += 1
        else:
            logger.warning(f"Product '{product['name']}' creation failed: {response.get('error', 'Unknown error')}")
    
    return created

def seed_data(clear_existing=False):
    """Main seeding function"""
    if clear_existing:
        clear_all_data()
    
    if not ProductCategory.objects.all():
        seed_categories()
    else:
        logger.info("Product categories already exist in the database.")
    
    if not Product.objects.all():
        seed_products()
    else:
        logger.info("Products already exist in the database.")