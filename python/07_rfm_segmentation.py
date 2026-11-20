import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from config import CFG, PROCESSED_DIR
from utils import load_clean_tables, save_plot, logger

def assign_segment(row: pd.Series) -> str:
    r, f, m = row["r_score"], row["f_score"], row["m_score"]
    if r >= 4 and f >= 4 and m >= 4: return "Champions"
    if r >= 3 and f >= 4: return "Loyal Customers"
    if r >= 4 and 2 <= f <= 3: return "Potential Loyalists"
    if r == 5 and f == 1: return "New Customers"
    if r <= 2 and f >= 4: return "At Risk / Cannot Lose"
    if r <= 2 and 2 <= f <= 3: return "Hibernating"
    return "Lost"

def run_rfm_segmentation() -> pd.DataFrame:
    tables = load_clean_tables()
    completed = tables["orders"][tables["orders"]["order_status"] == "Completed"].copy()
    ref_date = pd.to_datetime(CFG["rfm"]["reference_date"])
    rfm = completed.groupby("customer_id", as_index=False).agg(
        recency_days=("order_date", lambda x: (ref_date - x.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("total_amount", "sum"),
    )
    rfm["r_score"] = pd.qcut(rfm["recency_days"].rank(method="first"), q=5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["rfm_segment"] = rfm.apply(assign_segment, axis=1)
    rfm.to_csv(PROCESSED_DIR / "rfm_segments.csv", index=False)

    seg_sum = rfm.groupby("rfm_segment", as_index=False).agg(total_revenue=("monetary", "sum")).sort_values("total_revenue", ascending=False)
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(data=seg_sum, x="total_revenue", y="rfm_segment", ax=ax)
    ax.set_title("Total Revenue by RFM Segment", fontweight="bold")
    save_plot(fig, "05_rfm_segment_revenue.png")
    logger.info("RFM segmentation complete.")
    return rfm

if __name__ == "__main__":
    run_rfm_segmentation()
