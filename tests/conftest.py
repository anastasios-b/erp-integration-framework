"""
Pytest configuration and shared fixtures for ERP to Eshop integration tests
"""

import pytest
import tempfile
import os
import json


@pytest.fixture
def sample_erp_data():
    """Sample ERP product data for testing"""
    return {
        "products": [
            {
                "ItemId": "123",
                "ItemName": "Laptop X1000",
                "ItemDescription": "High-performance laptop with 16GB RAM",
                "ItemPrice": "999.99",
                "ItemSku": "LAPTOP-001",
                "ItemStock": "15"
            },
            {
                "ItemId": "456",
                "ItemName": "Wireless Mouse",
                "ItemDescription": "Ergonomic wireless mouse",
                "ItemPrice": "29.99",
                "ItemSku": "MOUSE-001",
                "ItemStock": "50"
            }
        ]
    }


@pytest.fixture
def sample_eshop_data():
    """Sample Eshop product data for testing"""
    return {
        "products": [
            {
                "id": 1001,
                "name": "Laptop X1000",
                "description": "High-performance laptop with 16GB RAM",
                "price": 899.99,
                "sku": "LAPTOP-001",
                "stock": 10
            },
            {
                "id": 1002,
                "name": "Wireless Mouse",
                "description": "Ergonomic wireless mouse",
                "price": 25.99,
                "sku": "MOUSE-001",
                "stock": 45
            },
            {
                "id": 1003,
                "name": "Orphan Product",
                "description": "Product with no ERP match",
                "price": 49.99,
                "sku": "ORPHAN-001",
                "stock": 5
            }
        ]
    }


@pytest.fixture
def temp_erp_file(sample_erp_data):
    """Create temporary ERP data file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_erp_data, f)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    if os.path.exists(temp_file):
        os.unlink(temp_file)


@pytest.fixture
def temp_eshop_file(sample_eshop_data):
    """Create temporary Eshop data file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_eshop_data, f)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    if os.path.exists(temp_file):
        os.unlink(temp_file)


@pytest.fixture
def temp_output_file():
    """Create temporary output file path"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    # Close the file so tests can write to it
    f.close()
    
    yield temp_file
    
    # Cleanup
    if os.path.exists(temp_file):
        os.unlink(temp_file)


@pytest.fixture
def temp_log_file():
    """Create temporary log file path"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
        temp_file = f.name
    
    # Close the file so tests can write to it
    f.close()
    
    yield temp_file
    
    # Cleanup
    if os.path.exists(temp_file):
        os.unlink(temp_file)


@pytest.fixture
def test_config():
    """Test configuration for sync operations"""
    return {
        "ERP_DATA_FILE": "test_erp.json",
        "ESHOP_DATA_FILE": "test_eshop.json",
        "OUTPUT_FILE": "test_output.json",
        "LOG_FILE": "test.log",
        "ERP_IDENTIFIER_FIELD": "ItemSku",
        "ESHOP_IDENTIFIER_FIELD": "sku",
        "FIELD_MAPPINGS": {
            "ItemName": "name",
            "ItemPrice": "price",
            "ItemDescription": "description",
            "ItemStock": "stock"
        },
        "VALIDATION_RULES": {
            "required_fields": ["id", "sku"],
            "positive_fields": ["price"],
            "non_null_fields": ["stock"]
        }
    }
