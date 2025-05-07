import unittest
from django.test import TestCase
from mongoengine import connect, disconnect
from ..models import Product, ProductCategory
from ..seed import seed_data
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()
from rest_framework.test import APIClient

class ProductIntegrationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        disconnect()
        connect(
            'product_db',
            host='mongodb://root:rootpassword@localhost:27017/product_db?authSource=admin',
            uuidRepresentation='standard'
        )
        seed_data()

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        disconnect()

    def test_creation_flow(self):
        categories = ProductCategory.objects.all()
        self.assertEqual(categories.count(), 5)
        
        products = Product.objects.all()
        self.assertEqual(products.count(), 6)
        
        product = Product.objects.first()
        self.assertIsNotNone(product.category)
        self.assertIsInstance(product.category, ProductCategory)

    def test_api_flow(self): 
        client = APIClient()
        client.login(username='root', password='rootpassword')
        
        from django.contrib.auth.models import User
        test_user=User.objects.create_user(username='testuser', password='testpassword')
        client.force_authenticate(user=test_user)
        
        response = client.get('/category/')
        self.assertEqual(response.status_code, 200)
        # print(response.data)
        self.assertEqual(len(response.data['data']), 6)
        
        response = client.get('/products/')
        self.assertEqual(response.status_code, 200)
        print(response.data['total_items'])
        self.assertEqual(response.data['total_items'],6) 
        
        response = client.get('/products/?title=Category 1')
        self.assertEqual(response.status_code, 200)
        print(response.data['total_items'])
        self.assertEqual(response.data['total_items'], 3)  

if __name__ == '__main__':
    unittest.main(verbosity=2)