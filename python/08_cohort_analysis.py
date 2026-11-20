import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from config import PROCESSED_DIR
from utils import load_clean_tables, save_plot, logger

def run_cohort_analysis() -> pd.DataFrame:
    tables = load_clean_tables()
    completed = tables["orders"][tables["orders"]["order_status"] == "Completed"].copy()
    completed["order_month"] = completed["order_date"].dt.to_period("M")
    completed["cohort_month"] = completed.groupby("customer_id")["order_date"].transform("min").dt.to_period("M")
    completed["cohort_index"] = (completed["order_month"].dt.year - completed["cohort_month"].dt.year) * 12 + (completed["order_month"].dt.month - completed["cohort_month"].dt.month)

    cohort_matrix = completed.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique().unstack(0).T
    retention = cohort_matrix.divide(cohort_matrix.iloc[:, 0], axis=0).iloc[:, :12] * 100
    retention.index = retention.index.astype(str)
    retention.round(2).to_csv(PROCESSED_DIR / "cohort_retention_matrix.csv")

    fig, ax = plt.subplots(figsize=(13, 8))
    sns.heatmap(retention.iloc[:15, :12], annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)
    ax.set_title("Monthly Customer Cohort Retention Matrix (%)", fontweight="bold")
    save_plot(fig, "06_cohort_retention_heatmap.png")
    logger.info("Cohort analysis complete.")
    return retention

if __name__ == "__main__":
    run_cohort_analysis()
