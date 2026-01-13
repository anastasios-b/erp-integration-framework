"""
Configuration settings for ERP to Eshop sync
"""

# File paths
ERP_DATA_FILE = "data/products_erp.json"
ESHOP_DATA_FILE = "data/products_eshop.json"
OUTPUT_FILE = "synced_from_erp.json"
LOG_FILE = "sync.log"

# Field identifiers
ERP_IDENTIFIER_FIELD = "ItemSku"
ESHOP_IDENTIFIER_FIELD = "sku"

# Field mapping from ERP to Eshop
FIELD_MAPPINGS = {
    "ItemName": "name",
    "ItemPrice": "price", 
    "ItemDescription": "description",
    "ItemStock": "stock"
}

# Validation rules
VALIDATION_RULES = {
    "required_fields": ["id", "sku"],
    "positive_fields": ["price"],
    "non_null_fields": ["stock"]
}
