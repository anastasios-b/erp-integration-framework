"""
Product data validation utilities
"""

from typing import Dict, Any, List

class ProductValidator:
    """Validates product data according to business rules"""
    
    def __init__(self, validation_rules: Dict[str, List[str]]):
        self.validation_rules = validation_rules
    
    def validate_product(self, product: Dict[str, Any]) -> List[str]:
        """Validate a single product and return list of errors"""
        errors = []
        
        # Check required fields
        for field in self.validation_rules.get("required_fields", []):
            if not product.get(field):
                errors.append(f"Missing {field}")
        
        # Check non-null fields
        for field in self.validation_rules.get("non_null_fields", []):
            if product.get(field) is None:
                errors.append(f"Missing {field}")
        
        # Check positive fields
        for field in self.validation_rules.get("positive_fields", []):
            value = product.get(field)
            if value is None:
                errors.append(f"Missing {field}")
            else:
                try:
                    numeric_value = float(value)
                    if numeric_value <= 0:
                        errors.append(f"Invalid {field}: must be greater than 0")
                except (ValueError, TypeError):
                    errors.append(f"Invalid {field} format: {value}")
        
        return errors
    
    def log_product_errors(self, product: Dict[str, Any], errors: List[str], start_timestamp: str, log_file: str):
        """Log validation errors for a product"""
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"[ERP to Eshop at {start_timestamp}] Product with Eshop ID {product.get('id')} could not be updated due to these errors:\n")
            for error in errors:
                log.write(f"    - {error}\n")
            log.write("\n")  # Add a blank line for readability
