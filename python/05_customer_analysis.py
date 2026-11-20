import matplotlib.pyplot as plt
import seaborn as sns
from config import PROCESSED_DIR
from utils import load_clean_tables, save_plot, logger

def run_customer_analysis() -> None:
    tables = load_clean_tables()
    customers, orders = tables["customers"], tables["orders"]
    completed = orders[orders["order_status"] == "Completed"]
    cust_metrics = completed.groupby("customer_id", as_index=False).agg(order_count=("order_id", "count"), lifetime_value=("total_amount", "sum"))
    cust_full = customers.merge(cust_metrics, on="customer_id", how="left").fillna({"order_count": 0, "lifetime_value": 0.0})
    cust_full["order_count"] = cust_full["order_count"].astype(int)
    cust_full.to_csv(PROCESSED_DIR / "customer_clv_summary.csv", index=False)

    ch_sum = cust_full.groupby("acquisition_channel", as_index=False).agg(avg_clv=("lifetime_value", "mean")).sort_values("avg_clv", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=ch_sum, x="avg_clv", y="acquisition_channel", ax=ax)
    ax.set_title("Average CLV by Acquisition Channel", fontweight="bold")
    save_plot(fig, "03_clv_by_channel.png")
    logger.info("Customer analysis complete.")

if __name__ == "__main__":
    run_customer_analysis()
