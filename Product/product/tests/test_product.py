import unittest
from unittest.mock import patch, MagicMock
from ..services import ProductService
from ..models import Product
from mongoengine import connect,disconnect
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

class TestProductService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        disconnect()
        connect(
            db='product_db',
            host='mongodb://root:rootpassword@localhost:27017/product_db?authSource=admin',
            uuidRepresentation='standard'
        )

    @patch('product.repositories.ProductRepository')
    def test_list_products(self, MockProductRepository):
        mock_repository = MagicMock()
        MockProductRepository.return_value = mock_repository
        mock_repository.find_all.return_value = [
            Product(name="Product1", price='10.0', category='1', description='Description1'),
            Product(name="Product2", price='20.0', category='2', description='Description2'),
            Product(name="Product3", price='30.0', category='3', description='Description3'),
            Product(name="Product4", price='40.0', category='4', description='Description4')
        ]

        product_service = ProductService(repository=mock_repository)
        products = product_service.list_products()

        for i in range(4):
            with self.subTest(i=i):
                self.assertEqual(products[i].name, f"Product{i+1}")

    @patch('product.repositories.ProductRepository')
    def test_get_product_by_id(self, MockProductRepository):
        mock_repository = MagicMock()
        MockProductRepository.return_value = mock_repository
        mock_repository.find_by_id.return_value = Product(name="Product1", price='10.0', category='70262a23e572822bb116a9b6', description='Description1')
        product_service = ProductService(repository=mock_repository)
        product = product_service.get_product_by_id('70262a23e572822bb116a9b6')
        if product['success']:
            self.assertEqual(product['data'].name, "Product1")
        else:
            self.assertEqual(product['error'], "Product not found")
    
    @patch('product.repositories.ProductRepository')
    def test_create_product(self, MockProductRepository):
        mock_repository = MagicMock()
        MockProductRepository.return_value = mock_repository
        mock_repository.create_product.return_value = {"success": True}
        product_service = ProductService(repository=mock_repository)
        status = product_service.create_product({"name": "Product1", "price": '10.0', "category": '680e096ddbd595451763ce82', "description": 'Description1'})
        # print(status)
        if status['success']:
            self.assertDictEqual(status, {"success": True})
        else:
            self.assertEqual(status['error'], "Category not found")
    
    @patch('product.repositories.ProductRepository')
    def test_update_product(self, MockProductRepository):
        mock_repository = MagicMock()
        MockProductRepository.return_value = mock_repository
        mock_repository.update.return_value = {"success": True}
        product_service = ProductService(repository=mock_repository)
        status = product_service.update_product({"name": "Product1", "price": '10.0', "category": '70262a23e572822bb116a9b6', "description": 'Description1'})
        if status['success']:
            self.assertDictEqual(status, {"success": True})
        else:
            self.assertEqual(status['success'],False)
    
    @patch('product.repositories.ProductRepository')
    def test_delete_product(self, MockProductRepository):
        mock_repository = MagicMock()
        MockProductRepository.return_value = mock_repository
        mock_repository.delete.return_value = {"success": True}
        product_service = ProductService(repository=mock_repository)
        status = product_service.delete_product('Product1')
        if status['success']:
            self.assertEqual(status['success'], True)
        else:
            self.assertEqual(status['success'], False)

    @patch('product.repositories.ProductRepository')
    def test_get_product_by_categoryID(self, MockProductRepository):
        mock_repository = MagicMock()
        MockProductRepository.return_value = mock_repository
        mock_repository.find_by_categoryID.return_value = [
            Product(name="Product1", price='10.0', category='70262a23e572822bb117a9b6', description='Description1'),
            Product(name="Product2", price='20.0', category='70262a23e572822bb117a9b6', description='Description2')
        ]
        product_service = ProductService(repository=mock_repository)
        products = product_service.get_products_by_categoryID('70262a23e572822bb117a9b6')
        with self.subTest():
            self.assertEqual(products['data'][0].name, "Product1")
            self.assertEqual(products['data'][1].name, "Product2")

    @classmethod
    def tearDownClass(cls):
        disconnect()

if __name__ == '__main__':
    unittest.main(verbosity=2)
