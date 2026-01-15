"""
ERP to Eshop Product Sync - Main Entry Point
"""

import logging
import sys
import os
import json

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config.settings import *
from src.product_sync import ProductSync

def setup_logging():
    """Configure logging for the application
    
    Raises:
        OSError: If log file cannot be created or written to
    """
    try:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_FILE, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    except OSError as e:
        print(f"Failed to setup logging: {e}")
        # Fallback to console-only logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )

def main():
    """Main application entry point
    
    Handles the complete product synchronization process with proper error handling
    and recovery mechanisms.
    """
    setup_logging()
    
    logging.info("Starting ERP to Eshop product sync")
    
    # Prepare configuration
    config = {
        "ERP_DATA_FILE": ERP_DATA_FILE,
        "ESHOP_DATA_FILE": ESHOP_DATA_FILE,
        "OUTPUT_FILE": OUTPUT_FILE,
        "LOG_FILE": LOG_FILE,
        "ERP_IDENTIFIER_FIELD": ERP_IDENTIFIER_FIELD,
        "ESHOP_IDENTIFIER_FIELD": ESHOP_IDENTIFIER_FIELD,
        "FIELD_MAPPINGS": FIELD_MAPPINGS,
        "VALIDATION_RULES": VALIDATION_RULES
    }
    
    try:
        # Initialize sync processor
        sync_processor = ProductSync(config)
        
        # Perform sync
        synced_products = sync_processor.sync_products()
        
        # Save results
        sync_processor.save_synced_products(synced_products)
        
        logging.info(f"Sync completed successfully. Processed {len(synced_products)} products.")
        
    except FileNotFoundError as e:
        logging.error(f"Configuration error - missing file: {e}")
        logging.error("Please check that all required data files exist and paths are correct.")
        sys.exit(2)
        
    except json.JSONDecodeError as e:
        logging.error(f"Data format error - invalid JSON: {e}")
        logging.error("Please check that all data files contain valid JSON format.")
        sys.exit(3)
        
    except ValueError as e:
        logging.error(f"Data validation error: {e}")
        logging.error("Please check data integrity and validation rules.")
        sys.exit(4)
        
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
        logging.error("Please check file and directory permissions.")
        sys.exit(5)
        
    except Exception as e:
        logging.error(f"Unexpected error during sync: {e}")
        logging.error("Please check the logs for more details and contact support if needed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
