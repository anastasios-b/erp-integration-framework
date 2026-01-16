# ERP to Eshop Product Integration Framework

A Python framework demonstrating robust product data synchronization between ERP systems and e-commerce platforms with comprehensive error handling, validation, and testing.

## Overview

This framework establishes ERP as the single source of truth for product information, synchronizing prices, stock levels, and descriptions to e-commerce platforms while implementing enterprise-grade error handling and data validation.

## Key Features

- **Data Integrity**: Comprehensive validation rules ensuring data quality
- **Graceful Error Handling**: Detailed logging with recovery mechanisms
- **Modular Architecture**: Clean separation of concerns for maintainability
- **Single File Solution**: All-in-one script for quick deployment and testing
- **Comprehensive Testing**: 30+ test cases ensuring reliability
- **Production-Ready Patterns**: Scalable design for enterprise integration
- **Detailed Logging**: Full audit trails for debugging and monitoring

## Architecture

### Core Components
- **DataLoader**: JSON file loading with error handling
- **FieldMapper**: Intelligent field mapping and type conversion
- **ProductValidator**: Business rule validation
- **ProductSync**: Orchestration of the sync process

### Data Flow
```
ERP Data → Validation → Field Mapping → Eshop Update → Logging
```

## Data Structures

### ERP Product Format
```json
{
  "products": [
    {
      "ItemSku": "PROD-0001",
      "ItemName": "Laptop X1000",
      "ItemPrice": "600.00",
      "ItemDescription": "High-performance laptop...",
      "ItemStock": "20"
    }
  ]
}
```

### Eshop Product Format
```json
{
  "products": [
    {
      "id": 8356,
      "sku": "PROD-0001",
      "name": "Laptop X1000",
      "price": 700.00,
      "description": "High-performance laptop...",
      "stock": 45
    }
  ]
}
```

### Field Mapping Configuration
| ERP Field | Eshop Field | Description |
|-----------|-------------|-------------|
| ItemSku | sku | Product identifier |
| ItemName | name | Product name |
| ItemPrice | price | Product price |
| ItemDescription | description | Product description |
| ItemStock | stock | Stock quantity |

## Quick Start

### Prerequisites
- Python 3.7+
- See `requirements.txt` for development dependencies

### Installation
```bash
# Clone the repository
git clone https://github.com/anastasios-b/erp-integration-framework.git
cd erp-integration-framework

# Install dependencies (optional for development)
pip install -r requirements.txt
```

### Running the Application
```bash
# Basic sync operation
python main.py

# Single-file version (all-in-one solution)
python single_file_script.py
```

### Running Tests
```bash
# Run all tests with detailed output
cd tests && python3 run_tests.py

# Or run specific test modules
python3 -m unittest tests.test_data_loader
python3 -m unittest tests.test_product_sync
python3 -m unittest tests.test_validator
```

## Project Structure

```
erp-integration-framework/
├── README.md                 # This file
├── main.py                   # Application entry point
├── single_file_script.py     # All-in-one single file solution
├── requirements.txt           # Python dependencies
├── .gitignore               # Git ignore patterns
├── config/
│   └── settings.py           # Configuration and validation rules
├── data/
│   ├── products_erp.json      # Sample ERP data
│   └── products_eshop.json    # Sample Eshop data
├── src/
│   ├── __init__.py
│   ├── data_loader.py         # File loading and JSON parsing
│   ├── field_mapper.py        # Field mapping and type conversion
│   ├── product_sync.py        # Core sync orchestration
│   └── validator.py           # Data validation logic
└── tests/
    ├── __init__.py
    ├── conftest.py           # Pytest fixtures
    ├── run_tests.py          # Test runner
    ├── test_data_loader.py    # DataLoader tests
    ├── test_product_sync.py    # ProductSync tests
    ├── test_validator.py       # Validator tests
    └── test_sync.py          # Legacy tests
```

## Output Files

- `synced_from_erp.json`: Successfully synchronized products (from main.py)
- `single_file_synced_from_erp.json`: Successfully synchronized products (from single_file_script.py)
- `sync.log`: Comprehensive logging with timestamps and error details (from main.py)
- `single_file_sync.log`: Comprehensive logging with timestamps and error details (from single_file_script.py)

## Configuration

### Validation Rules
```python
VALIDATION_RULES = {
    "required_fields": ["id", "sku"],      # Must be present
    "positive_fields": ["price"],            # Must be > 0
    "non_null_fields": ["stock"]             # Cannot be None
}
```

### Field Mappings
```python
FIELD_MAPPINGS = {
    "ItemName": "name",
    "ItemPrice": "price",
    "ItemDescription": "description",
    "ItemStock": "stock"
}
```

## Testing

The framework includes comprehensive test coverage:

- **30+ test cases** across all components
- **Error scenario testing** for edge cases
- **Mock-based testing** for isolated unit tests
- **Integration testing** for end-to-end workflows

### Test Categories
- Data loading and parsing
- Field mapping and type conversion
- Validation logic
- Sync orchestration
- Error handling

## Current Limitations

- **Prototype Implementation**: Uses local JSON files instead of live APIs
- **One-way Sync**: ERP → Eshop only (no bidirectional sync)
- **File-based Storage**: No database persistence
- **Manual Execution**: No automated scheduling
- **Basic Recovery**: Limited retry mechanisms

## Production Roadmap

### Immediate Enhancements
- [ ] Real API integration (REST/GraphQL)
- [ ] Database persistence for sync history
- [ ] Incremental sync with change detection
- [ ] Configuration-driven field mappings
- [ ] Docker containerization

### Advanced Features
- [ ] Bidirectional synchronization
- [ ] Real-time change detection
- [ ] Monitoring and alerting
- [ ] Rollback capabilities
- [ ] Performance optimization for large datasets
- [ ] Multi-tenant support

## Contributing

Contributions are welcome! Feel free to:
- Fork the repository
- Submit pull requests
- Report issues
- Suggest improvements
- Help evolve this into a production-grade solution

## License

This project is open source and available under the MIT License.

## Links

- **Issues**: https://github.com/anastasios-b/erp-integration-framework/issues
- **Creator's Portfolio**: https://anastasios-bolkas.tech

---

**Built with ❤️ for reliable enterprise data integration**
