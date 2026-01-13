"""
Basic tests for ERP to Eshop sync functionality
"""

import unittest
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.field_mapper import FieldMapper
from src.validator import ProductValidator

class TestFieldMapper(unittest.TestCase):
    
    def setUp(self):
        self.field_mappings = {
            "ItemName": "name",
            "ItemPrice": "price",
            "ItemStock": "stock"
        }
        self.erp_field_types = {"ItemName": "str", "ItemPrice": "float", "ItemStock": "int"}
        self.eshop_field_types = {"name": "str", "price": "float", "stock": "int"}
        
        self.mapper = FieldMapper(self.field_mappings, self.erp_field_types, self.eshop_field_types)
    
    def test_cast_to_eshop_type(self):
        """Test type casting functionality"""
        # Test string casting
        result = self.mapper.cast_to_eshop_type("test", "name")
        self.assertEqual(result, "test")
        
        # Test int casting
        result = self.mapper.cast_to_eshop_type("20", "stock")
        self.assertEqual(result, 20)
        
        # Test float casting
        result = self.mapper.cast_to_eshop_type("29.99", "price")
        self.assertEqual(result, 29.99)
    
    def test_map_product_fields(self):
        """Test field mapping between ERP and Eshop products"""
        erp_product = {
            "ItemName": "Test Product",
            "ItemPrice": 99.99,
            "ItemStock": 10
        }
        eshop_product = {
            "id": 123,
            "sku": "TEST-001"
        }
        
        result = self.mapper.map_product_fields(erp_product, eshop_product)
        
        expected = {
            "id": 123,
            "sku": "TEST-001",
            "name": "Test Product",
            "price": 99.99,
            "stock": 10
        }
        
        self.assertEqual(result, expected)

class TestProductValidator(unittest.TestCase):
    
    def setUp(self):
        self.validation_rules = {
            "required_fields": ["id", "sku"],
            "positive_fields": ["price"],
            "non_null_fields": ["stock"]
        }
        self.validator = ProductValidator(self.validation_rules)
    
    def test_validate_valid_product(self):
        """Test validation of a valid product"""
        product = {
            "id": 123,
            "sku": "TEST-001",
            "price": 29.99,
            "stock": 10
        }
        
        errors = self.validator.validate_product(product)
        self.assertEqual(len(errors), 0)
    
    def test_validate_missing_required_fields(self):
        """Test validation when required fields are missing"""
        product = {
            "price": 29.99,
            "stock": 10
        }
        
        errors = self.validator.validate_product(product)
        self.assertTrue(any("Missing id" in error for error in errors))
        self.assertTrue(any("Missing sku" in error for error in errors))
    
    def test_validate_invalid_price(self):
        """Test validation when price is invalid"""
        product = {
            "id": 123,
            "sku": "TEST-001",
            "price": -10,
            "stock": 10
        }
        
        errors = self.validator.validate_product(product)
        self.assertTrue(any("Invalid price" in error for error in errors))
    
    def test_validate_missing_stock(self):
        """Test validation when stock is null"""
        product = {
            "id": 123,
            "sku": "TEST-001",
            "price": 29.99,
            "stock": None
        }
        
        errors = self.validator.validate_product(product)
        self.assertTrue(any("Missing stock" in error for error in errors))

if __name__ == '__main__':
    unittest.main()
