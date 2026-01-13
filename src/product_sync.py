"""
Core product synchronization logic
"""

import json
import logging
from typing import Dict, Any, List
from .data_loader import DataLoader
from .field_mapper import FieldMapper
from .validator import ProductValidator

class ProductSync:
    """Orchestrates the product synchronization process"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_loader = DataLoader(config["LOG_FILE"])
        self.validator = ProductValidator(config["VALIDATION_RULES"])
        
    def sync_products(self) -> List[Dict[str, Any]]:
        """Main sync process - returns list of successfully synced products"""
        
        # Load data
        erp_products = self.data_loader.load_erp_products(self.config["ERP_DATA_FILE"])
        eshop_products = self.data_loader.load_eshop_products(self.config["ESHOP_DATA_FILE"])
        
        # Get field types
        erp_field_types = self.data_loader.get_field_types(erp_products)
        eshop_field_types = self.data_loader.get_field_types(eshop_products)
        
        # Initialize field mapper
        field_mapper = FieldMapper(
            self.config["FIELD_MAPPINGS"],
            erp_field_types,
            eshop_field_types
        )
        
        # Process each Eshop product
        updated_eshop_products = []
        
        for eshop_product in eshop_products:
            eshop_sku = eshop_product.get(self.config["ESHOP_IDENTIFIER_FIELD"])
            if not eshop_sku:
                continue
            
            # Find matching ERP product
            matching_erp_product = self._find_matching_erp_product(
                erp_products, eshop_sku, self.config["ERP_IDENTIFIER_FIELD"]
            )
            
            if not matching_erp_product:
                logging.warning(f"Product with SKU {eshop_sku} found in Eshop but missing in ERP")
                continue
            
            # Map fields from ERP to Eshop
            updated_product = field_mapper.map_product_fields(matching_erp_product, eshop_product)
            
            # Validate the updated product
            validation_errors = self.validator.validate_product(updated_product)
            
            if validation_errors:
                self.validator.log_product_errors(
                    updated_product, 
                    validation_errors, 
                    self.data_loader.start_timestamp,
                    self.config["LOG_FILE"]
                )
                continue
            
            updated_eshop_products.append(updated_product)
        
        return updated_eshop_products
    
    def _find_matching_erp_product(self, erp_products: List[Dict[str, Any]], sku: str, identifier_field: str) -> Dict[str, Any]:
        """Find ERP product matching the given SKU"""
        return next(
            (erp_product for erp_product in erp_products 
             if erp_product.get(identifier_field) == sku),
            None
        )
    
    def save_synced_products(self, products: List[Dict[str, Any]]):
        """Save successfully synced products to output file"""
        try:
            with open(self.config["OUTPUT_FILE"], "w", encoding="utf-8") as outfile:
                json.dump(products, outfile, indent=4, ensure_ascii=False)
            logging.info(f"Successfully synced {len(products)} products to {self.config['OUTPUT_FILE']}")
        except Exception as e:
            logging.error(f"Failed to write synced products file: {e}")
