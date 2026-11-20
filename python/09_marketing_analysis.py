import matplotlib.pyplot as plt
import seaborn as sns
from config import PROCESSED_DIR
from utils import load_clean_tables, save_plot, logger

def run_marketing_analysis() -> None:
    tables = load_clean_tables()
    completed = tables["orders"][tables["orders"]["order_status"] == "Completed"]
    attr = completed.groupby("campaign_id", as_index=False).agg(attributed_orders=("order_id", "nunique"), acquired_customers=("customer_id", "nunique"), attributed_revenue=("total_amount", "sum"))
    camp_perf = tables["campaigns"].merge(attr, on="campaign_id", how="left").fillna(0)
    camp_perf["ctr_pct"] = (camp_perf["clicks"] / camp_perf["impressions"] * 100).round(2)
    camp_perf["roas"] = (camp_perf["attributed_revenue"] / camp_perf["budget"]).round(2)
    camp_perf["cac"] = (camp_perf["budget"] / camp_perf["acquired_customers"].replace(0, 1)).round(2)
    camp_perf = camp_perf.sort_values("roas", ascending=False)
    camp_perf.to_csv(PROCESSED_DIR / "campaign_performance.csv", index=False)

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(data=camp_perf, x="roas", y="campaign_name", hue="channel", dodge=False, ax=ax)
    ax.axvline(3.0, color="red", linestyle="--", label="Target ROAS (3.0x)")
    ax.set_title("Marketing Campaign ROAS", fontweight="bold")
    save_plot(fig, "07_campaign_roas.png")
    logger.info("Marketing analysis complete.")

if __name__ == "__main__":
    run_marketing_analysis()
