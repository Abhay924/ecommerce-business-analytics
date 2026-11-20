from pathlib import Path
import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config.yaml"

def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {
        "project": {"random_seed": 42},
        "paths": {
            "raw_data": "data/raw",
            "processed_data": "data/processed",
            "charts": "reports/charts",
            "excel_output": "excel/ecommerce_analysis.xlsx",
        },
        "data_generation": {
            "num_customers": 2500,
            "num_products": 150,
            "num_campaigns": 12,
            "num_orders": 15000,
            "start_date": "2024-01-01",
            "end_date": "2025-12-31",
        },
        "rfm": {"reference_date": "2026-01-01", "quantiles": 5},
    }

CFG = load_config()
RANDOM_SEED = CFG["project"].get("random_seed", 42)
RAW_DIR = ROOT_DIR / CFG["paths"]["raw_data"]
PROCESSED_DIR = ROOT_DIR / CFG["paths"]["processed_data"]
CHARTS_DIR = ROOT_DIR / CFG["paths"]["charts"]
EXCEL_PATH = ROOT_DIR / CFG["paths"]["excel_output"]

for directory in [RAW_DIR, PROCESSED_DIR, CHARTS_DIR, EXCEL_PATH.parent]:
    directory.mkdir(parents=True, exist_ok=True)
