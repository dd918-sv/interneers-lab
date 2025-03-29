from django.apps import AppConfig
from mongoengine import connect


connect(
    db='product_db',
    host='mongodb://root:rootpassword@localhost:27017/product_db?authSource=admin'
)

class ProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "product"
