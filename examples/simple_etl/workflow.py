"""Simple ETL Pipeline using Graflow.

This workflow demonstrates:
- Parallel data extraction from CSV and JSON files
- Filtering and aggregation transformations
- Channel-based inter-task communication
"""

import csv
import json
from pathlib import Path

from graflow.core.context import TaskExecutionContext
from graflow.core.decorators import task
from graflow.core.workflow import workflow


# Data directory relative to this file
DATA_DIR = Path(__file__).parent / "data"


@task(inject_context=True)
def extract_csv(ctx: TaskExecutionContext) -> list[dict]:
    """Extract sales data from CSV file."""
    csv_path = DATA_DIR / "sales.csv"
    records = []

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "product_id": int(row["product_id"]),
                "product_name": row["product_name"],
                "quantity": int(row["quantity"]),
                "price": float(row["price"]),
                "date": row["date"],
            })

    print(f"[extract_csv] Loaded {len(records)} sales records")
    ctx.get_channel().set("csv_data", records)
    return records


@task(inject_context=True)
def extract_json(ctx: TaskExecutionContext) -> list[dict]:
    """Extract inventory data from JSON file."""
    json_path = DATA_DIR / "inventory.json"

    with open(json_path) as f:
        records = json.load(f)

    print(f"[extract_json] Loaded {len(records)} inventory records")
    ctx.get_channel().set("json_data", records)
    return records


@task(inject_context=True)
def filter_data(ctx: TaskExecutionContext) -> dict:
    """Filter sales data: keep only records with quantity >= 50."""
    channel = ctx.get_channel()
    csv_data = channel.get("csv_data")
    json_data = channel.get("json_data")

    # Filter sales with quantity >= 50
    filtered_sales = [r for r in csv_data if r["quantity"] >= 50]

    # Filter inventory with stock above reorder level
    filtered_inventory = [r for r in json_data if r["stock"] > r["reorder_level"]]

    filtered = {
        "sales": filtered_sales,
        "inventory": filtered_inventory,
    }

    print(f"[filter_data] Filtered to {len(filtered_sales)} sales, {len(filtered_inventory)} inventory items")
    channel.set("filtered_data", filtered)
    return filtered


@task(inject_context=True)
def aggregate_data(ctx: TaskExecutionContext) -> dict:
    """Aggregate filtered data into summary statistics."""
    channel = ctx.get_channel()
    filtered = channel.get("filtered_data")

    sales = filtered["sales"]
    inventory = filtered["inventory"]

    # Sales aggregation
    total_revenue = sum(r["quantity"] * r["price"] for r in sales)
    total_quantity = sum(r["quantity"] for r in sales)
    unique_products = len(set(r["product_id"] for r in sales))

    # Inventory aggregation
    total_stock = sum(r["stock"] for r in inventory)
    warehouses = set(r["warehouse"] for r in inventory)

    aggregated = {
        "sales_metrics": {
            "total_revenue": round(total_revenue, 2),
            "total_quantity": total_quantity,
            "unique_products": unique_products,
            "record_count": len(sales),
        },
        "inventory_metrics": {
            "total_stock": total_stock,
            "item_count": len(inventory),
            "warehouse_count": len(warehouses),
        },
    }

    print(f"[aggregate_data] Aggregated metrics computed")
    channel.set("aggregated_results", aggregated)
    return aggregated


@task(inject_context=True)
def load_console(ctx: TaskExecutionContext) -> None:
    """Display aggregated results to console."""
    channel = ctx.get_channel()
    results = channel.get("aggregated_results")

    print("\n" + "=" * 50)
    print("         ETL PIPELINE RESULTS")
    print("=" * 50)

    print("\n📊 Sales Metrics:")
    sales = results["sales_metrics"]
    print(f"   Total Revenue:    ${sales['total_revenue']:,.2f}")
    print(f"   Total Quantity:   {sales['total_quantity']:,}")
    print(f"   Unique Products:  {sales['unique_products']}")
    print(f"   Records Processed:{sales['record_count']}")

    print("\n📦 Inventory Metrics:")
    inv = results["inventory_metrics"]
    print(f"   Total Stock:      {inv['total_stock']:,}")
    print(f"   Items in Stock:   {inv['item_count']}")
    print(f"   Warehouses:       {inv['warehouse_count']}")

    print("\n" + "=" * 50)


def run_etl():
    """Execute the ETL pipeline."""
    with workflow("simple_etl") as wf:
        # Create task instances with explicit task_ids for parallel group
        csv_task = extract_csv(task_id="extract_csv")
        json_task = extract_json(task_id="extract_json")
        filter_task = filter_data(task_id="filter_data")
        aggregate_task = aggregate_data(task_id="aggregate_data")
        load_task = load_console(task_id="load_console")

        # Define task graph: parallel extraction -> filter -> aggregate -> load
        (csv_task | json_task).set_group_name("extractors") >> filter_task >> aggregate_task >> load_task

        # Execute starting from the parallel extraction group
        wf.execute("extractors")


if __name__ == "__main__":
    run_etl()
