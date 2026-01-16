# This file includes the whole ERP integration framework utilities in one file.
# Running it will result in the same integration result as the full framework.

import logging
import json

# Setup logging first
LOG_FILE = "./single_file_sync.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# File paths
ERP_DATA_FILE = "./data/products_erp.json"
ESHOP_DATA_FILE = "./data/products_eshop.json"
OUTPUT_FILE = "./single_file_synced_from_erp.json"

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

# Initiate empty variables to hold the products
erp_products = []
eshop_products = []

# Receive ERP products
try:
    with open(ERP_DATA_FILE, "r", encoding="utf-8") as f:
        erp_response = json.load(f)
    
    if not erp_response.get("products") or len(erp_response["products"]) == 0:
        logging.error("No products found in ERP response")
        raise ValueError("No products found in ERP response")
        
    erp_products = erp_response["products"]
    
except FileNotFoundError:
    logging.error(f"ERP products file not found: {ERP_DATA_FILE}")
    raise
except json.JSONDecodeError as e:
    logging.error(f"Invalid JSON in ERP products file: {e}")
    raise

# Query eshop products
try:
    with open(ESHOP_DATA_FILE, "r", encoding="utf-8") as f:
        eshop_response = json.load(f)
    
    if not eshop_response.get("products") or len(eshop_response["products"]) == 0:
        logging.error("No products found in Eshop response")
        raise ValueError("No products found in Eshop response")
        
    eshop_products = eshop_response["products"]
    
except FileNotFoundError:
    logging.error(f"Eshop products file not found: {ESHOP_DATA_FILE}")
    raise
except json.JSONDecodeError as e:
    logging.error(f"Invalid JSON in Eshop products file: {e}")
    raise

# Validate eshop product data
for eshop_product in eshop_products:
    errors = []
    # Check required fields
    for field in VALIDATION_RULES.get("required_fields", []):
        if not eshop_product.get(field):
            errors.append(f"Missing {field}")
    
    # Check non-null fields
    for field in VALIDATION_RULES.get("non_null_fields", []):
        if eshop_product.get(field) is None:
            errors.append(f"Missing {field}")
    
    # Check positive fields
    for field in VALIDATION_RULES.get("positive_fields", []):
        value = eshop_product.get(field)
        if value is None:
            errors.append(f"Missing {field}")
        else:
            try:
                numeric_value = float(value)
                if numeric_value <= 0:
                    errors.append(f"Invalid {field}: must be greater than 0")
            except (ValueError, TypeError):
                errors.append(f"Invalid {field} format: {value}")
    
    if errors:
        logging.error(f"Validation errors for product {eshop_product.get('id')}: {errors}")

# ERP products don't need initial validation - they will be validated after mapping
# The validation rules are for the final Eshop format, not the raw ERP format

# Get field types for type casting
def get_field_types(products):
    if not products:
        return {}
    field_types = {}
    for key, value in products[0].items():
        field_types[key] = type(value).__name__
    return field_types

erp_field_types = get_field_types(erp_products)
eshop_field_types = get_field_types(eshop_products)

def cast_to_eshop_type(value, eshop_field):
    """Cast a value to the expected Eshop field type"""
    if value is None:
        return None
        
    target_type = eshop_field_types.get(eshop_field, type(value).__name__)
    
    try:
        if target_type == "str":
            return str(value)
        elif target_type == "int":
            return int(value)
        elif target_type == "float":
            return float(value)
        elif target_type == "bool":
            return bool(value)
        elif target_type == "list":
            return list(value)
        elif target_type == "dict":
            return dict(value)
        else:
            return value
    except Exception as e:
        logging.warning(f"Failed to cast value {value} to type {target_type}: {e}")
        return value

# Map fields and update products
updated_eshop_products = []

for eshop_product in eshop_products:
    eshop_sku = eshop_product.get(ESHOP_IDENTIFIER_FIELD)
    if not eshop_sku:
        logging.warning(f"Eshop product missing SKU field: {ESHOP_IDENTIFIER_FIELD}")
        continue
    
    # Find matching ERP product
    matching_erp_product = None
    for erp_product in erp_products:
        if erp_product.get(ERP_IDENTIFIER_FIELD) == eshop_sku:
            matching_erp_product = erp_product
            break
    
    if not matching_erp_product:
        logging.warning(f"Product with SKU {eshop_sku} found in Eshop but missing in ERP")
        continue
    
    # Create mapped product
    mapped_product = {}
    
    # Copy identifier fields
    mapped_product["id"] = eshop_product.get("id")
    mapped_product["sku"] = eshop_product.get("sku")
    
    # Map fields according to configuration
    for erp_field, eshop_field in FIELD_MAPPINGS.items():
        erp_value = matching_erp_product.get(erp_field, eshop_product.get(eshop_field))
        mapped_product[eshop_field] = cast_to_eshop_type(erp_value, eshop_field)
    
    # Validate the mapped product
    errors = []
    
    # Check required fields
    for field in VALIDATION_RULES.get("required_fields", []):
        if not mapped_product.get(field):
            errors.append(f"Missing {field}")
    
    # Check non-null fields
    for field in VALIDATION_RULES.get("non_null_fields", []):
        if mapped_product.get(field) is None:
            errors.append(f"Missing {field}")
    
    # Check positive fields
    for field in VALIDATION_RULES.get("positive_fields", []):
        value = mapped_product.get(field)
        if value is None:
            errors.append(f"Missing {field}")
        else:
            try:
                numeric_value = float(value)
                if numeric_value <= 0:
                    errors.append(f"Invalid {field}: must be greater than 0")
            except (ValueError, TypeError):
                errors.append(f"Invalid {field} format: {value}")
    
    if errors:
        logging.error(f"Validation errors for mapped product {mapped_product.get('id')}: {errors}")
        continue
    
    updated_eshop_products.append(mapped_product)

# Save results
try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        json.dump(updated_eshop_products, outfile, indent=4, ensure_ascii=False)
    logging.info(f"Successfully synced {len(updated_eshop_products)} products to {OUTPUT_FILE}")
    print(f"Sync completed successfully. Processed {len(updated_eshop_products)} products.")
except Exception as e:
    logging.error(f"Failed to write synced products file: {e}")
    print(f"Error: Failed to save results - {e}")
    exit(1)