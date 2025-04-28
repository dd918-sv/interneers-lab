import unittest
from unittest.mock import patch, MagicMock
from product.services import ProductCategoryService
from product.models import ProductCategory
from mongoengine import connect, disconnect
import os, django

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

class TestProductCategoryService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        disconnect()
        connect(
            db='product_db',
            host='mongodb://root:rootpassword@localhost:27017/product_db?authSource=admin',
            uuidRepresentation='standard'
        )

    @patch('product.repositories.ProductCategoryRepository')
    def test_list_product_categories(self,MockProductCategoryRepository):
        mock_repository=MagicMock()
        MockProductCategoryRepository.return_value=mock_repository

        mock_repository.find_all_categories.return_value = [
            ProductCategory(title="category 1",description="Description1"),
            ProductCategory(title="category 2",description="Description2"),
        ]

        product_category_service=ProductCategoryService(repository=mock_repository)
        categories=product_category_service.list_product_categories()

        self.assertEqual(categories[0].title,"category 1")
        self.assertEqual(categories[1].title,"category 2")

    @patch('product.repositories.ProductCategoryRepository')
    def test_get_category_by_name(self,MockProductCategoryRepository):
        mock_repository=MagicMock()
        MockProductCategoryRepository.return_value=mock_repository

        mock_repository.find_by_name.return_value = ProductCategory(title="category 1",description="Description1")
        product_category_service=ProductCategoryService(repository=mock_repository)

        category=product_category_service.get_category_by_name("category 1")
        self.assertEqual(category.title,"category 1")

    @patch('product.repositories.ProductCategoryRepository')
    def test_create_product_category(self, MockProductCategoryRepository):

        mock_repository = MagicMock()
        MockProductCategoryRepository.return_value = mock_repository
        
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = {"title": "Category 1", "description": "Description1"}
        
        mock_repository.create_product_category.return_value = {
            "success": True,
            "data": {"title": "Category 1", "description": "Description1"}
        }
        
        with patch('product.services.ProductCategorySerializer', return_value=mock_serializer):
            service = ProductCategoryService(repository=mock_repository)
            status = service.create_product_category({
                "title": "Category 1",
                "description": "Description1"
            })
        
        self.assertTrue(status['success'])
        mock_repository.create_product_category.assert_called_once_with(mock_serializer)

    
    @patch('product.repositories.ProductCategoryRepository')
    def test_update_category(self,MockProductCategoryRepository):
        mock_repository=MagicMock()
        MockProductCategoryRepository.return_value=mock_repository

        mock_repository.update_category.return_value={"success":True}
        product_category_service=ProductCategoryService(repository=mock_repository)
        mock_repository.find_by_name.return_value = ProductCategory(title="Category 1",description="Description1")

        status=product_category_service.update_category({"title":'Category 1',"description":'Description1'})
        self.assertDictEqual(status,{"success":True})
    
    @patch('product.repositories.ProductCategoryRepository')
    def test_delete_product_category(self,MockProductCategoryRepository):
        mock_repository=MagicMock()
        MockProductCategoryRepository.return_value=mock_repository

        mock_repository.delete_product_category.return_value={"success":True}
        product_category_service=ProductCategoryService(repository=mock_repository)
        mock_repository.find_by_name.return_value = ProductCategory(title="Category 1",description="Description1")
        
        status=product_category_service.delete_product_category("category 1")
        self.assertDictEqual(status,{"success":True})

    @classmethod
    def tearDownClass(cls):
        disconnect()

if __name__ == '__main__':
    unittest.main()
