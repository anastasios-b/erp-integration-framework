"""
Unit tests for ProductValidator class
"""

import unittest
from src.validator import ProductValidator


class TestProductValidator(unittest.TestCase):
    """Test cases for ProductValidator functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validation_rules = {
            "required_fields": ["id", "sku", "name"],
            "positive_fields": ["price"],
            "non_null_fields": ["stock"]
        }
        self.validator = ProductValidator(self.validation_rules)
        
        # Valid product for testing
        self.valid_product = {
            "id": 123,
            "sku": "TEST-001",
            "name": "Test Product",
            "price": 99.99,
            "stock": 10
        }
    
    def test_validate_product_valid(self):
        """Test validation of a valid product"""
        errors = self.validator.validate_product(self.valid_product)
        self.assertEqual(len(errors), 0)
    
    def test_validate_product_missing_required_fields(self):
        """Test validation with missing required fields"""
        invalid_product = {
            "id": 123,
            # Missing "sku" and "name"
            "price": 99.99
        }
        
        errors = self.validator.validate_product(invalid_product)
        self.assertEqual(len(errors), 2)
        self.assertIn("Missing sku", errors)
        self.assertIn("Missing name", errors)
    
    def test_validate_product_empty_required_fields(self):
        """Test validation with empty required fields"""
        invalid_product = {
            "id": 123,
            "sku": "",  # Empty string
            "name": "Test Product",
            "price": 99.99
        }
        
        errors = self.validator.validate_product(invalid_product)
        self.assertEqual(len(errors), 1)
        self.assertIn("Missing sku", errors)
    
    def test_validate_product_null_fields(self):
        """Test validation with null fields"""
        invalid_product = {
            "id": 123,
            "sku": "TEST-001",
            "name": "Test Product",
            "price": 99.99,
            "stock": None  # Null value
        }
        
        errors = self.validator.validate_product(invalid_product)
        self.assertEqual(len(errors), 1)
        self.assertIn("Missing stock", errors)
    
    def test_validate_product_negative_price(self):
        """Test validation with negative price"""
        invalid_product = {
            "id": 123,
            "sku": "TEST-001",
            "name": "Test Product",
            "price": -10.0,  # Negative price
            "stock": 10
        }
        
        errors = self.validator.validate_product(invalid_product)
        self.assertEqual(len(errors), 1)
        self.assertIn("Invalid price: must be greater than 0", errors)
    
    def test_validate_product_zero_price(self):
        """Test validation with zero price"""
        invalid_product = {
            "id": 123,
            "sku": "TEST-001",
            "name": "Test Product",
            "price": 0,  # Zero price
            "stock": 10
        }
        
        errors = self.validator.validate_product(invalid_product)
        self.assertEqual(len(errors), 1)
        self.assertIn("Invalid price: must be greater than 0", errors)
    
    def test_validate_product_invalid_price_format(self):
        """Test validation with invalid price format"""
        invalid_product = {
            "id": 123,
            "sku": "TEST-001",
            "name": "Test Product",
            "price": "not_a_number",  # Invalid format
            "stock": 10
        }
        
        errors = self.validator.validate_product(invalid_product)
        self.assertEqual(len(errors), 1)
        self.assertIn("Invalid price format: not_a_number", errors)
    
    def test_validate_product_missing_positive_field(self):
        """Test validation with missing positive field"""
        invalid_product = {
            "id": 123,
            "sku": "TEST-001",
            "name": "Test Product",
            # Missing "price"
            "stock": 10
        }
        
        errors = self.validator.validate_product(invalid_product)
        self.assertEqual(len(errors), 1)
        self.assertIn("Missing price", errors)
    
    def test_validate_product_string_price(self):
        """Test validation with string representation of positive number"""
        valid_product = {
            "id": 123,
            "sku": "TEST-001",
            "name": "Test Product",
            "price": "99.99",  # String that can be converted to float
            "stock": 10
        }
        
        errors = self.validator.validate_product(valid_product)
        self.assertEqual(len(errors), 0)
    
    def test_log_product_errors(self):
        """Test error logging functionality"""
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            log_file = f.name
        
        try:
            product = {"id": 123, "sku": "TEST-001"}
            errors = ["Missing name", "Invalid price"]
            
            self.validator.log_product_errors(product, errors, "2026-01-15 01:00:00", log_file)
            
            with open(log_file, 'r') as f:
                log_content = f.read()
            
            self.assertIn("Product with Eshop ID 123", log_content)
            self.assertIn("Missing name", log_content)
            self.assertIn("Invalid price", log_content)
            
        finally:
            os.unlink(log_file)


if __name__ == '__main__':
    unittest.main()
