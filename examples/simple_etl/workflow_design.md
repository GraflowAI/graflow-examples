# Workflow Design: Simple ETL

## Overview
CSVファイルとJSONファイルからデータを並列で読み込み、集計・変換処理を行い、結果をコンソールに出力するシンプルなETLワークフロー。

## Tasks

| Task ID | Responsibility | Inputs | Outputs |
|---------|---------------|--------|---------|
| extract_csv | CSVファイルからデータを読み込む | ファイルパス | レコードのリスト |
| extract_json | JSONファイルからデータを読み込む | ファイルパス | レコードのリスト |
| transform | データの集計・変換処理 | 抽出されたデータ | 変換後のデータ |
| load | 結果をコンソールに出力 | 変換後のデータ | なし |

## Task Graph
```
(extract_csv | extract_json) >> transform >> load
```

```
┌─────────────┐
│ extract_csv │──┐
└─────────────┘  │
                 ├──► transform ──► load
┌──────────────┐ │
│ extract_json │─┘
└──────────────┘
```

## Channel Data Flow

| Channel Key | Producer | Consumer | Description |
|-------------|----------|----------|-------------|
| csv_data | extract_csv | transform | CSVから抽出したレコード |
| json_data | extract_json | transform | JSONから抽出したレコード |
| transformed_data | transform | load | 変換後のデータ |

## サンプルデータ構造

**CSVデータ例** (`data/sales.csv`):
```csv
id,product,quantity,price
1,Apple,10,100
2,Banana,20,50
3,Orange,15,80
```

**JSONデータ例** (`data/inventory.json`):
```json
[
  {"id": 1, "product": "Apple", "stock": 100},
  {"id": 2, "product": "Banana", "stock": 200},
  {"id": 3, "product": "Orange", "stock": 150}
]
```

## Transform処理の詳細

1. CSVとJSONのデータをproduct名で結合
2. 各商品の売上額（quantity × price）を計算
3. 在庫状況と合わせてサマリーを作成

## Error Handling
- ファイルが存在しない場合: エラーメッセージを出力して空のデータを返す
- データ形式が不正な場合: 該当レコードをスキップしてログ出力
