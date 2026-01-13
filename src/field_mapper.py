"""
Field mapping and type conversion utilities
"""

import logging
from typing import Dict, Any, List

class FieldMapper:
    """Handles field mapping and type conversion between ERP and Eshop"""
    
    def __init__(self, field_mappings: Dict[str, str], erp_field_types: Dict[str, str], eshop_field_types: Dict[str, str]):
        self.field_mappings = field_mappings
        self.erp_field_types = erp_field_types
        self.eshop_field_types = eshop_field_types
    
    def cast_to_eshop_type(self, value: Any, eshop_field: str) -> Any:
        """Cast a value to the expected Eshop field type"""
        if value is None:
            return None
            
        target_type = self.eshop_field_types.get(eshop_field, type(value).__name__)
        
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
                return value  # fallback, no conversion
        except Exception as e:
            logging.warning(f"Failed to cast value {value} to type {target_type}: {e}")
            return value  # fallback if conversion fails
    
    def map_product_fields(self, erp_product: Dict[str, Any], eshop_product: Dict[str, Any]) -> Dict[str, Any]:
        """Map fields from ERP product to Eshop product format"""
        mapped_product = {}
        
        # Copy identifier fields
        mapped_product["id"] = eshop_product.get("id")
        mapped_product["sku"] = eshop_product.get("sku")
        
        # Map fields according to configuration
        for erp_field, eshop_field in self.field_mappings.items():
            erp_value = erp_product.get(erp_field, eshop_product.get(eshop_field))
            mapped_product[eshop_field] = self.cast_to_eshop_type(erp_value, eshop_field)
        
        return mapped_product
