import matplotlib.pyplot as plt
import seaborn as sns
from config import PROCESSED_DIR
from utils import load_clean_tables, save_plot, logger

def run_product_analysis() -> None:
    tables = load_clean_tables()
    merged = tables["order_items"].merge(tables["orders"][["order_id", "order_status"]], on="order_id").merge(tables["products"][["product_id", "category"]], on="product_id")
    comp = merged[merged["order_status"] == "Completed"]
    cat_perf = comp.groupby("category", as_index=False).agg(units_sold=("quantity", "sum"), net_revenue=("line_total", "sum"), gross_margin=("line_margin", "sum"))
    cat_perf["margin_pct"] = (cat_perf["gross_margin"] / cat_perf["net_revenue"] * 100).round(2)
    cat_perf = cat_perf.sort_values("net_revenue", ascending=False)
    cat_perf.to_csv(PROCESSED_DIR / "category_performance.csv", index=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=cat_perf, x="category", y="net_revenue", label="Net Revenue", ax=ax)
    sns.barplot(data=cat_perf, x="category", y="gross_margin", label="Gross Profit", color="navy", ax=ax)
    ax.set_title("Revenue vs. Gross Profit by Category", fontweight="bold")
    ax.legend()
    save_plot(fig, "04_category_revenue_margin.png")
    logger.info("Product analysis complete.")

if __name__ == "__main__":
    run_product_analysis()
