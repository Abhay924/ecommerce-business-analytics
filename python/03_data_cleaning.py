import pandas as pd
from config import RAW_DIR, PROCESSED_DIR
from utils import logger

def clean_all_datasets() -> None:
    cust = pd.read_csv(RAW_DIR / "customers_raw.csv").drop_duplicates(subset=["customer_id"], keep="first").copy()
    cust["acquisition_channel"] = cust["acquisition_channel"].astype(str).str.strip()
    cust["gender"] = cust["gender"].fillna("Unspecified")
    cust["age"] = cust["age"].clip(lower=18, upper=95)
    cust.to_csv(PROCESSED_DIR / "customers_clean.csv", index=False)

    prod = pd.read_csv(RAW_DIR / "products_raw.csv").drop_duplicates(subset=["product_id"], keep="first").copy()
    prod["unit_price"] = prod[["unit_price", "unit_cost"]].max(axis=1)
    prod.to_csv(PROCESSED_DIR / "products_clean.csv", index=False)

    camp = pd.read_csv(RAW_DIR / "campaigns_raw.csv").drop_duplicates(subset=["campaign_id"], keep="first").copy()
    camp.to_csv(PROCESSED_DIR / "campaigns_clean.csv", index=False)

    orders = pd.read_csv(RAW_DIR / "orders_raw.csv").drop_duplicates(subset=["order_id"], keep="first").copy()
    orders["payment_method"] = orders["payment_method"].fillna("Credit Card")
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    orders = orders[orders["customer_id"].isin(cust["customer_id"])]
    orders.to_csv(PROCESSED_DIR / "orders_clean.csv", index=False)

    items = pd.read_csv(RAW_DIR / "order_items_raw.csv").drop_duplicates(subset=["order_item_id"], keep="first").copy()
    items = items[items["order_id"].isin(orders["order_id"]) & items["product_id"].isin(prod["product_id"])]
    items["quantity"] = items["quantity"].clip(lower=1)
    items.to_csv(PROCESSED_DIR / "order_items_clean.csv", index=False)
    logger.info("All 5 cleaned datasets saved to data/processed/.")

if __name__ == "__main__":
    clean_all_datasets()
