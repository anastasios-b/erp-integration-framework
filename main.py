"""
ERP to Eshop Product Sync - Main Entry Point
"""

import logging
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config.settings import *
from src.product_sync import ProductSync

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def main():
    """Main application entry point"""
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
        
    except Exception as e:
        logging.error(f"Sync failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
