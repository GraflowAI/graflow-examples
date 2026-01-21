# Simple ETL Workflow

## Overview

CSVファイルとJSONファイルからデータを並列で読み込み、集計・変換処理を行い、結果をコンソールに出力するシンプルなETLワークフローです。

- 売上データ（CSV）と在庫データ（JSON）を結合
- 各商品の売上額を計算
- 販売後の在庫数を算出

## Requirements

- Python 3.11+
- Graflow

## Usage

### Basic Execution

```bash
PYTHONPATH=. uv run python examples/simple_etl/workflow.py
```

### With Custom Data Files

```python
from examples.simple_etl.workflow import run_etl

result = run_etl(
    csv_path="path/to/your/sales.csv",
    json_path="path/to/your/inventory.json"
)
```

## Workflow Structure

### Task Graph

```
┌─────────────┐
│ extract_csv │──┐
└─────────────┘  │
                 ├──► transform ──► load
┌──────────────┐ │
│ extract_json │─┘
└──────────────┘
```

### Tasks

| Task | Description |
|------|-------------|
| extract_csv | CSVファイルから売上データを読み込む |
| extract_json | JSONファイルから在庫データを読み込む |
| transform | データの結合・集計・変換を行う |
| load | 結果をコンソールに整形出力する |

### Channel Data Flow

| Channel Key | Producer | Consumer | Description |
|-------------|----------|----------|-------------|
| csv_data | extract_csv | transform | CSVから抽出した売上レコード |
| json_data | extract_json | transform | JSONから抽出した在庫レコード |
| transformed_data | transform | load | 結合・変換後のデータ |

## Data Format

### Input: sales.csv

```csv
id,product,quantity,price
1,Apple,10,100
2,Banana,20,50
```

### Input: inventory.json

```json
[
  {"id": 1, "product": "Apple", "stock": 100},
  {"id": 2, "product": "Banana", "stock": 200}
]
```

### Output

```
============================================================
ETL Result - Sales Summary with Inventory
============================================================
Product      Qty   Price    Revenue   Stock   After
------------------------------------------------------------
Apple         10     100       1000     100      90
Banana        20      50       1000     200     180
------------------------------------------------------------
Total Revenue:                            2000
============================================================
```

## Example Output

```
Extracted 5 records from CSV
Extracted 5 records from JSON
Transformed 5 records

============================================================
ETL Result - Sales Summary with Inventory
============================================================
Product      Qty   Price    Revenue   Stock   After
------------------------------------------------------------
Apple         10     100       1000     100      90
Banana        20      50       1000     200     180
Orange        15      80       1200     150     135
Grape          8     200       1600      50      42
Melon          5     300       1500      30      25
------------------------------------------------------------
Total Revenue:                            6300
============================================================

Processed 5 records successfully.
```
