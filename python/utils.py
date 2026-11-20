import logging
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from config import PROCESSED_DIR, CHARTS_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("ecommerce_analytics")

plt.rcParams["figure.figsize"] = (11, 6)
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
sns.set_palette("deep")

def save_plot(fig: plt.Figure, filename: str) -> Path:
    output_path = CHARTS_DIR / filename
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved chart -> {output_path.name}")
    return output_path

def load_clean_tables() -> dict[str, pd.DataFrame]:
    tables = {}
    for name in ["customers", "products", "campaigns", "orders", "order_items"]:
        file_path = PROCESSED_DIR / f"{name}_clean.csv"
        if not file_path.exists():
            raise FileNotFoundError(f"Missing {file_path}. Run 01_generate_dataset.py and 03_data_cleaning.py first.")
        tables[name] = pd.read_csv(file_path)
    tables["orders"]["order_date"] = pd.to_datetime(tables["orders"]["order_date"])
    tables["customers"]["signup_date"] = pd.to_datetime(tables["customers"]["signup_date"])
    return tables
