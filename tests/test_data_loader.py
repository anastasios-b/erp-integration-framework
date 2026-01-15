"""
Unit tests for DataLoader class
"""

import unittest
import json
import tempfile
import os
from unittest.mock import patch, mock_open
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    """Test cases for DataLoader functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_log_file = "test.log"
        self.loader = DataLoader(self.test_log_file)
        
        # Sample test data
        self.valid_erp_data = {
            "products": [
                {
                    "ItemId": "123",
                    "ItemName": "Test Product",
                    "ItemPrice": "100.00",
                    "ItemSku": "TEST-001",
                    "ItemStock": "10"
                }
            ]
        }
        
        self.valid_eshop_data = {
            "products": [
                {
                    "id": 456,
                    "name": "Test Product",
                    "price": 99.99,
                    "sku": "TEST-001",
                    "stock": 5
                }
            ]
        }
    
    def test_load_erp_products_success(self):
        """Test successful loading of ERP products"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.valid_erp_data, f)
            temp_file = f.name
        
        try:
            products = self.loader.load_erp_products(temp_file)
            self.assertEqual(len(products), 1)
            self.assertEqual(products[0]["ItemSku"], "TEST-001")
        finally:
            os.unlink(temp_file)
    
    def test_load_erp_products_file_not_found(self):
        """Test handling of missing ERP file"""
        with self.assertRaises(FileNotFoundError):
            self.loader.load_erp_products("nonexistent_file.json")
    
    def test_load_erp_products_invalid_json(self):
        """Test handling of invalid JSON in ERP file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json}')
            temp_file = f.name
        
        try:
            with self.assertRaises(json.JSONDecodeError):
                self.loader.load_erp_products(temp_file)
        finally:
            os.unlink(temp_file)
    
    def test_load_erp_products_empty_products(self):
        """Test handling of empty products array"""
        empty_data = {"products": []}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(empty_data, f)
            temp_file = f.name
        
        try:
            with self.assertRaises(ValueError) as context:
                self.loader.load_erp_products(temp_file)
            self.assertIn("No products found", str(context.exception))
        finally:
            os.unlink(temp_file)
    
    def test_load_eshop_products_success(self):
        """Test successful loading of Eshop products"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.valid_eshop_data, f)
            temp_file = f.name
        
        try:
            products = self.loader.load_eshop_products(temp_file)
            self.assertEqual(len(products), 1)
            self.assertEqual(products[0]["sku"], "TEST-001")
        finally:
            os.unlink(temp_file)
    
    def test_get_field_types_success(self):
        """Test successful field type extraction"""
        products = [
            {"id": 1, "name": "Test", "price": 10.5, "active": True}
        ]
        
        field_types = self.loader.get_field_types(products)
        
        expected_types = {
            "id": "int",
            "name": "str", 
            "price": "float",
            "active": "bool"
        }
        
        self.assertEqual(field_types, expected_types)
    
    def test_get_field_types_empty_products(self):
        """Test handling of empty products list"""
        with self.assertRaises(ValueError) as context:
            self.loader.get_field_types([])
        self.assertIn("No products available", str(context.exception))


if __name__ == '__main__':
    unittest.main()
