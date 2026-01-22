# Workflow Design: Simple ETL Pipeline

## Overview
A demonstration ETL workflow that extracts data from CSV and JSON files in parallel, applies filtering and aggregation transformations, and outputs results to the console.

## Use Case
Process sales data from a CSV file and inventory data from a JSON file, filter relevant records, aggregate metrics, and display a summary report.

## Tasks

| Task ID | Responsibility | Inputs | Outputs |
|---------|---------------|--------|---------|
| extract_csv | Read and parse CSV file | File path | List of records |
| extract_json | Read and parse JSON file | File path | List of records |
| filter_data | Filter records based on criteria | Raw records | Filtered records |
| aggregate_data | Calculate summary statistics | Filtered records | Aggregated metrics |
| load_console | Display results to console | Aggregated metrics | None (side effect) |

## Task Graph

```
extract_csv ──┐
              ├──> filter_data >> aggregate_data >> load_console
extract_json ─┘
```

ASCII representation with operators:
```
(extract_csv | extract_json) >> filter_data >> aggregate_data >> load_console
```

## Channel Data Flow

| Channel Key | Producer | Consumer | Description |
|-------------|----------|----------|-------------|
| csv_data | extract_csv | filter_data | Raw records from CSV |
| json_data | extract_json | filter_data | Raw records from JSON |
| filtered_data | filter_data | aggregate_data | Records after filtering |
| aggregated_results | aggregate_data | load_console | Summary statistics |

## Sample Data Structure

### CSV Input (sales.csv)
```csv
product_id,product_name,quantity,price,date
1,Widget A,100,9.99,2024-01-15
2,Widget B,50,19.99,2024-01-16
```

### JSON Input (inventory.json)
```json
[
  {"product_id": 1, "stock": 500, "warehouse": "A"},
  {"product_id": 2, "stock": 200, "warehouse": "B"}
]
```

## Error Handling

- **Strategy**: Fail-fast with descriptive error messages
- File not found: Raise clear error with file path
- Parse errors: Log and skip malformed records
- Empty data: Proceed with warning message

## Expected Output

```
=== ETL Pipeline Results ===
Total Sales Records: 10
Total Inventory Items: 5
Filtered Records: 8
Aggregated Metrics:
  - Total Revenue: $1,234.56
  - Total Quantity Sold: 150
  - Products in Stock: 5
```
