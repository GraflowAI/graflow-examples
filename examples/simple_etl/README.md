# Simple ETL Pipeline

## Overview

A demonstration ETL (Extract-Transform-Load) workflow that processes sales and inventory data using Graflow. This example showcases parallel data extraction, filtering, aggregation, and console output.

## Requirements

- Python 3.11+
- Graflow

## Usage

### Basic Execution

```bash
PYTHONPATH=. uv run python examples/simple_etl/workflow.py
```

### Programmatic Usage

```python
from examples.simple_etl.workflow import run_etl

run_etl()
```

## Workflow Structure

### Task Graph

```
extract_csv ──┐
              ├──> filter_data >> aggregate_data >> load_console
extract_json ─┘
```

Using Graflow operators:
```python
(extract_csv | extract_json) >> filter_data >> aggregate_data >> load_console
```

### Tasks

| Task | Description |
|------|-------------|
| `extract_csv` | Reads sales data from `data/sales.csv` |
| `extract_json` | Reads inventory data from `data/inventory.json` |
| `filter_data` | Filters sales (qty >= 50) and inventory (stock > reorder level) |
| `aggregate_data` | Computes summary statistics (revenue, quantities, stock) |
| `load_console` | Displays formatted results to console |

### Channel Data Flow

| Channel Key | Producer | Consumer | Description |
|-------------|----------|----------|-------------|
| `csv_data` | extract_csv | filter_data | Raw sales records |
| `json_data` | extract_json | filter_data | Raw inventory records |
| `filtered_data` | filter_data | aggregate_data | Filtered records |
| `aggregated_results` | aggregate_data | load_console | Summary statistics |

## Data Files

### sales.csv

Sales transaction data with fields:
- `product_id`: Product identifier
- `product_name`: Product name
- `quantity`: Units sold
- `price`: Unit price
- `date`: Transaction date

### inventory.json

Inventory status with fields:
- `product_id`: Product identifier
- `product_name`: Product name
- `stock`: Current stock level
- `warehouse`: Warehouse location
- `reorder_level`: Minimum stock threshold

## Example Output

```
[extract_csv] Loaded 10 sales records
[extract_json] Loaded 5 inventory records
[filter_data] Filtered to 6 sales, 5 inventory items
[aggregate_data] Aggregated metrics computed

==================================================
         ETL PIPELINE RESULTS
==================================================

📊 Sales Metrics:
   Total Revenue:    $6,120.05
   Total Quantity:   495
   Unique Products:  3
   Records Processed:6

📦 Inventory Metrics:
   Total Stock:      955
   Items in Stock:   5
   Warehouses:       3

==================================================
```
