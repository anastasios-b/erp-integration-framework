"""
Unit tests for ProductSync class
"""

import unittest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.product_sync import ProductSync


class TestProductSync(unittest.TestCase):
    """Test cases for ProductSync functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = {
            "ERP_DATA_FILE": "test_erp.json",
            "ESHOP_DATA_FILE": "test_eshop.json",
            "OUTPUT_FILE": "test_output.json",
            "LOG_FILE": "test.log",
            "ERP_IDENTIFIER_FIELD": "ItemSku",
            "ESHOP_IDENTIFIER_FIELD": "sku",
            "FIELD_MAPPINGS": {
                "ItemName": "name",
                "ItemPrice": "price",
                "ItemStock": "stock"
            },
            "VALIDATION_RULES": {
                "required_fields": ["id", "sku"],
                "positive_fields": ["price"],
                "non_null_fields": ["stock"]
            }
        }
        
        self.sync = ProductSync(self.config)
        
        # Sample test data
        self.erp_products = [
            {
                "ItemId": "123",
                "ItemName": "Updated Product",
                "ItemPrice": "150.00",
                "ItemSku": "TEST-001",
                "ItemStock": "25"
            }
        ]
        
        self.eshop_products = [
            {
                "id": 456,
                "name": "Old Product",
                "price": 100.00,
                "sku": "TEST-001",
                "stock": 10
            }
        ]
    
    @patch('src.product_sync.DataLoader')
    def test_sync_products_success(self, mock_data_loader_class):
        """Test successful product synchronization"""
        # Mock DataLoader instance
        mock_loader = MagicMock()
        mock_loader.load_erp_products.return_value = self.erp_products
        mock_loader.load_eshop_products.return_value = self.eshop_products
        mock_loader.get_field_types.return_value = {"ItemSku": "str", "sku": "str"}
        mock_loader.start_timestamp = "2026-01-15 01:00:00"
        mock_data_loader_class.return_value = mock_loader
        
        # Create new sync instance with mocked DataLoader
        sync = ProductSync(self.config)
        
        # Perform sync
        result = sync.sync_products()
        
        # Verify results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Updated Product")
        self.assertEqual(result[0]["price"], 150.0)
        self.assertEqual(result[0]["stock"], 25)
    
    @patch('src.product_sync.DataLoader')
    def test_sync_products_missing_erp_product(self, mock_data_loader_class):
        """Test handling of missing ERP product"""
        # Eshop product with no matching ERP product
        eshop_products = [
            {
                "id": 456,
                "name": "Orphan Product",
                "price": 100.00,
                "sku": "MISSING-001",
                "stock": 10
            }
        ]
        
        mock_loader = MagicMock()
        mock_loader.load_erp_products.return_value = self.erp_products
        mock_loader.load_eshop_products.return_value = eshop_products
        mock_loader.get_field_types.return_value = {"ItemSku": "str", "sku": "str"}
        mock_loader.start_timestamp = "2026-01-15 01:00:00"
        mock_data_loader_class.return_value = mock_loader
        
        sync = ProductSync(self.config)
        
        with patch('src.product_sync.logging') as mock_logging:
            result = sync.sync_products()
            
            # Should return empty list since no matches found
            self.assertEqual(len(result), 0)
            # Should log warning about missing product
            mock_logging.warning.assert_called_with(
                "Product with SKU MISSING-001 found in Eshop but missing in ERP"
            )
    
    @patch('src.product_sync.DataLoader')
    def test_sync_products_validation_failure(self, mock_data_loader_class):
        """Test handling of validation failures"""
        # Mock validator to return errors
        with patch('src.product_sync.ProductValidator') as mock_validator_class:
            mock_validator = MagicMock()
            mock_validator.validate_product.return_value = ["Invalid price"]
            mock_validator_class.return_value = mock_validator
            
            mock_loader = MagicMock()
            mock_loader.load_erp_products.return_value = self.erp_products
            mock_loader.load_eshop_products.return_value = self.eshop_products
            mock_loader.get_field_types.return_value = {"ItemSku": "str", "sku": "str"}
            mock_loader.start_timestamp = "2026-01-15 01:00:00"
            mock_data_loader_class.return_value = mock_loader
            
            sync = ProductSync(self.config)
            
            result = sync.sync_products()
            
            # Should return empty list due to validation failure
            self.assertEqual(len(result), 0)
            # Validator should be called
            mock_validator.validate_product.assert_called()
    
    def test_find_matching_erp_product_success(self):
        """Test successful ERP product matching"""
        result = self.sync._find_matching_erp_product(
            self.erp_products, 
            "TEST-001", 
            "ItemSku"
        )
        
        self.assertIsNotNone(result)
        self.assertEqual(result["ItemSku"], "TEST-001")
    
    def test_find_matching_erp_product_not_found(self):
        """Test ERP product not found"""
        result = self.sync._find_matching_erp_product(
            self.erp_products, 
            "NONEXISTENT", 
            "ItemSku"
        )
        
        self.assertIsNone(result)
    
    def test_save_synced_products_success(self):
        """Test successful saving of synced products"""
        products = [
            {"id": 1, "sku": "TEST-001", "name": "Test Product"}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Update config to use temp file
            self.config["OUTPUT_FILE"] = temp_file
            sync = ProductSync(self.config)
            
            sync.save_synced_products(products)
            
            # Verify file was written correctly
            with open(temp_file, 'r') as f:
                saved_data = json.load(f)
            
            self.assertEqual(len(saved_data), 1)
            self.assertEqual(saved_data[0]["sku"], "TEST-001")
            
        finally:
            os.unlink(temp_file)
    
    def test_save_synced_products_file_error(self):
        """Test handling of file write errors"""
        products = [{"id": 1, "sku": "TEST-001"}]
        
        # Use invalid file path to trigger error
        self.config["OUTPUT_FILE"] = "/invalid/path/output.json"
        sync = ProductSync(self.config)
        
        with patch('src.product_sync.logging') as mock_logging:
            sync.save_synced_products(products)
            
            # Should log error but not crash
            mock_logging.error.assert_called()
            error_call = mock_logging.error.call_args[0][0]
            self.assertIn("Failed to write synced products file", error_call)


if __name__ == '__main__':
    unittest.main()
