import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_clean_tables, save_plot, logger

def run_eda() -> None:
    tables = load_clean_tables()
    orders, items = tables["orders"], tables["order_items"]
    completed = orders[orders["order_status"] == "Completed"].copy()
    completed = completed.merge(items.groupby("order_id", as_index=False)["line_margin"].sum(), on="order_id", how="left")
    completed["year_month"] = completed["order_date"].dt.to_period("M").astype(str)

    monthly = completed.groupby("year_month", as_index=False).agg(revenue=("total_amount", "sum"), margin=("line_margin", "sum"))
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly["year_month"], monthly["revenue"], marker="o", label="Net Revenue ($)")
    ax.plot(monthly["year_month"], monthly["margin"], marker="s", label="Gross Profit ($)")
    ax.set_title("Monthly Net Revenue & Gross Margin Trend", fontweight="bold")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    save_plot(fig, "01_monthly_revenue_trend.png")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=completed, x="device_type", y="total_amount", showfliers=False, ax=ax)
    ax.set_title("Order Value Distribution by Device Type", fontweight="bold")
    save_plot(fig, "02_aov_by_device.png")
    logger.info("EDA complete.")

if __name__ == "__main__":
    run_eda()
