"""
Simple ETL Workflow

CSVファイルとJSONファイルからデータを並列で読み込み、
集計・変換処理を行い、結果をコンソールに出力するワークフロー。

Task Graph:
    (extract_csv | extract_json) >> transform >> load
"""

import csv
import json
from pathlib import Path

from graflow.core.context import TaskExecutionContext
from graflow.core.decorators import task
from graflow.core.workflow import workflow


# データディレクトリのパス
DATA_DIR = Path(__file__).parent / "data"


@task(inject_context=True)
def extract_csv(ctx: TaskExecutionContext, file_path: str) -> list[dict]:
    """CSVファイルからデータを読み込む"""
    path = Path(file_path)
    if not path.exists():
        print(f"Warning: CSV file not found: {file_path}")
        return []

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            data.append({
                "id": int(row["id"]),
                "product": row["product"],
                "quantity": int(row["quantity"]),
                "price": int(row["price"]),
            })

    print(f"Extracted {len(data)} records from CSV")
    ctx.get_channel().set("csv_data", data)
    return data


@task(inject_context=True)
def extract_json(ctx: TaskExecutionContext, file_path: str) -> list[dict]:
    """JSONファイルからデータを読み込む"""
    path = Path(file_path)
    if not path.exists():
        print(f"Warning: JSON file not found: {file_path}")
        return []

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    print(f"Extracted {len(data)} records from JSON")
    ctx.get_channel().set("json_data", data)
    return data


@task(inject_context=True)
def transform(ctx: TaskExecutionContext) -> list[dict]:
    """データの集計・変換処理を行う"""
    channel = ctx.get_channel()
    csv_data = channel.get("csv_data", [])
    json_data = channel.get("json_data", [])

    # JSONデータを商品名でインデックス化
    inventory_by_product = {item["product"]: item["stock"] for item in json_data}

    # CSVデータと結合して集計
    transformed = []
    for sale in csv_data:
        product = sale["product"]
        quantity = sale["quantity"]
        price = sale["price"]
        stock = inventory_by_product.get(product, 0)

        transformed.append({
            "product": product,
            "quantity": quantity,
            "price": price,
            "revenue": quantity * price,
            "stock": stock,
            "stock_after_sale": stock - quantity,
        })

    print(f"Transformed {len(transformed)} records")
    channel.set("transformed_data", transformed)
    return transformed


@task(inject_context=True)
def load(ctx: TaskExecutionContext) -> None:
    """結果をコンソールに出力する"""
    channel = ctx.get_channel()
    data = channel.get("transformed_data", [])

    print("\n" + "=" * 60)
    print("ETL Result - Sales Summary with Inventory")
    print("=" * 60)

    # ヘッダー
    print(f"{'Product':<10} {'Qty':>5} {'Price':>7} {'Revenue':>10} {'Stock':>7} {'After':>7}")
    print("-" * 60)

    # データ行
    total_revenue = 0
    for item in data:
        print(
            f"{item['product']:<10} "
            f"{item['quantity']:>5} "
            f"{item['price']:>7} "
            f"{item['revenue']:>10} "
            f"{item['stock']:>7} "
            f"{item['stock_after_sale']:>7}"
        )
        total_revenue += item["revenue"]

    print("-" * 60)
    print(f"{'Total Revenue:':<35} {total_revenue:>10}")
    print("=" * 60)


def run_etl(
    csv_path: str | None = None,
    json_path: str | None = None,
) -> list[dict]:
    """ETLワークフローを実行する

    Args:
        csv_path: CSVファイルのパス（デフォルト: data/sales.csv）
        json_path: JSONファイルのパス（デフォルト: data/inventory.json）

    Returns:
        変換後のデータリスト
    """
    csv_path = csv_path or str(DATA_DIR / "sales.csv")
    json_path = json_path or str(DATA_DIR / "inventory.json")

    with workflow("simple_etl") as wf:
        # タスクインスタンスを作成（パラメータをバインド）
        csv_task = extract_csv(task_id="extract_csv", file_path=csv_path)
        json_task = extract_json(task_id="extract_json", file_path=json_path)

        # タスクグラフを構築
        (csv_task | json_task).set_group_name("extract") >> transform >> load

        # ワークフローを実行
        result, exec_ctx = wf.execute("extract", ret_context=True)

        # 変換後のデータを返す
        return exec_ctx.get_channel().get("transformed_data", [])


if __name__ == "__main__":
    result = run_etl()
    print(f"\nProcessed {len(result)} records successfully.")
