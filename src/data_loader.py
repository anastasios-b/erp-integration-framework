"""
Data loading utilities for ERP and Eshop products
"""

import json
import logging
from typing import Dict, List, Any
from datetime import datetime

class DataLoader:
    """Handles loading and parsing of product data from JSON files"""
    
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.start_timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
    def load_erp_products(self, file_path: str) -> List[Dict[str, Any]]:
        """Load products from ERP JSON file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                erp_response = json.load(f)
            
            if not erp_response.get("products") or len(erp_response["products"]) == 0:
                logging.error("No products found in ERP response")
                exit(1)
                
            return erp_response["products"]
            
        except FileNotFoundError:
            logging.error(f"ERP products file not found: {file_path}")
            exit(1)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in ERP products file: {e}")
            exit(1)
    
    def load_eshop_products(self, file_path: str) -> List[Dict[str, Any]]:
        """Load products from Eshop JSON file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                eshop_response = json.load(f)
            
            if not eshop_response.get("products") or len(eshop_response["products"]) == 0:
                logging.error("No products found in Eshop response")
                exit(1)
                
            return eshop_response["products"]
            
        except FileNotFoundError:
            logging.error(f"Eshop products file not found: {file_path}")
            exit(1)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in Eshop products file: {e}")
            exit(1)
    
    def get_field_types(self, products: List[Dict[str, Any]]) -> Dict[str, str]:
        """Extract field types from a list of products"""
        if not products:
            logging.error("No products available to determine field types")
            exit(1)
            
        field_types = {}
        for key, value in products[0].items():
            field_types[key] = type(value).__name__
        
        return field_types
