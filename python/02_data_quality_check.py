import pandas as pd
from config import RAW_DIR
from utils import logger

def run_quality_checks() -> dict:
    report = {}
    files = {
        "customers": ("customers_raw.csv", "customer_id"),
        "products": ("products_raw.csv", "product_id"),
        "campaigns": ("campaigns_raw.csv", "campaign_id"),
        "orders": ("orders_raw.csv", "order_id"),
        "order_items": ("order_items_raw.csv", "order_item_id"),
    }
    loaded = {}
    for name, (fname, pk) in files.items():
        df = pd.read_csv(RAW_DIR / fname)
        loaded[name] = df
        dup_pk = int(df.duplicated(subset=[pk]).sum())
        null_counts = {col: int(cnt) for col, cnt in df.isnull().sum().items() if cnt > 0}
        report[name] = {"row_count": len(df), "duplicate_pks": dup_pk, "null_columns": null_counts}
        logger.info(f"[AUDIT] {name.upper():12s} | Rows: {len(df):6d} | Duplicate PKs: {dup_pk:3d} | Nulls: {null_counts}")
    return report

if __name__ == "__main__":
    run_quality_checks()
