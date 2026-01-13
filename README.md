# ERP to Eshop Product Sync Prototype

A Python prototype that demonstrates product data synchronization between an ERP system and an e-commerce platform.

## Overview

This prototype loads product data from ERP and Eshop JSON files, validates the presence of products in both datasets, and syncs product information from ERP (source of truth) to Eshop.

## Assumptions

1. **ERP is the source of truth** for product information (name, price, description, stock)
2. **Products are identified by SKU** - `ItemSku` in ERP, `sku` in Eshop
3. **Eshop may have products not in ERP** - these are logged but don't cause sync failure
4. **Field mapping is predefined** - ERP fields map to specific Eshop fields
5. **Data types must match** - ERP values are cast to Eshop field types
6. **Sync is one-way** - ERP → Eshop only

## Use Cases

### Primary Use Case
- **Product Information Sync**: Update Eshop product details (name, price, description, stock) from ERP data

### Edge Cases Handled
- **Missing ERP products**: Log warning and continue processing other products
- **Type conversion failures**: Fallback to original value and log warning
- **Malformed data**: Log specific validation errors and skip problematic products
- **File not found**: Log error and exit gracefully

## Data Structure

### ERP Product Format
```json
{
  "products": [
    {
      "ItemSku": "PROD-0001",
      "ItemName": "Laptop X1000",
      "ItemPrice": 600.0,
      "ItemDescription": "High-performance laptop...",
      "ItemStock": 20
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

### Field Mapping
| ERP Field | Eshop Field | Description |
|-----------|-------------|-------------|
| ItemSku | sku | Product identifier |
| ItemName | name | Product name |
| ItemPrice | price | Product price |
| ItemDescription | description | Product description |
| ItemStock | stock | Stock quantity |

## Example Usage

```bash
python main.py
```

## Output Files

- `synced_from_erp.json`: Successfully synced products
- `sync_errors.log`: Error and warning messages

## Architecture

```
final_version/
├── README.md                 # This file
├── main.py                   # Entry point and orchestration
├── config/
│   └── settings.py           # Configuration and field mappings
├── data/
│   ├── products_erp.json     # Sample ERP data
│   └── products_eshop.json   # Sample Eshop data
├── src/
│   ├── __init__.py
│   ├── data_loader.py        # File loading and JSON parsing
│   ├── field_mapper.py       # Field mapping and type conversion
│   ├── product_sync.py       # Core sync logic
│   └── validator.py          # Data validation
└── tests/
    ├── __init__.py
    └── test_sync.py          # Basic tests
```

## Limitations

- **Prototype only**: Uses local JSON files instead of real APIs
- **No authentication**: No security considerations implemented
- **Single run**: No incremental sync or change detection
- **Basic error handling**: Limited retry mechanisms
- **No database**: In-memory processing only

## Future Enhancements

- Real API integration (REST/GraphQL)
- Database persistence for sync history
- Incremental sync with change detection
- Configuration-driven field mappings
- Comprehensive test suite
- Docker containerization
- Monitoring and alerting
- Rollback capabilities

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)
