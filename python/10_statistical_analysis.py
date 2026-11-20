import pandas as pd
from scipy import stats
from config import PROCESSED_DIR
from utils import load_clean_tables, logger

def run_statistical_tests() -> pd.DataFrame:
    tables = load_clean_tables()
    orders, customers = tables["orders"], tables["customers"]
    completed = orders[orders["order_status"] == "Completed"]
    results = []

    d_aov = completed.loc[completed["device_type"] == "Desktop", "total_amount"]
    m_aov = completed.loc[completed["device_type"] == "Mobile", "total_amount"]
    t_stat, p_t = stats.ttest_ind(d_aov, m_aov, equal_var=False)
    results.append({"test_name": "Welch Two-Sample t-Test (Desktop vs Mobile AOV)", "statistic": round(float(t_stat), 4), "p_value": float(p_t), "significant_at_0_05": bool(p_t < 0.05), "interpretation": f"Desktop (${d_aov.mean():.2f}) vs Mobile (${m_aov.mean():.2f})"})

    clv_df = customers[["customer_id", "acquisition_channel"]].merge(completed.groupby("customer_id", as_index=False)["total_amount"].sum(), on="customer_id", how="left").fillna(0)
    f_stat, p_f = stats.f_oneway(*[grp["total_amount"].values for _, grp in clv_df.groupby("acquisition_channel")])
    results.append({"test_name": "One-Way ANOVA (CLV across Acquisition Channels)", "statistic": round(float(f_stat), 4), "p_value": float(p_f), "significant_at_0_05": bool(p_f < 0.05), "interpretation": "Variance across 5 channels"})

    sub = orders[orders["order_status"].isin(["Completed", "Returned"])]
    chi2, p_c, _, _ = stats.chi2_contingency(pd.crosstab(sub["device_type"], sub["order_status"]))
    results.append({"test_name": "Chi-Square Independence Test (Device vs Return)", "statistic": round(float(chi2), 4), "p_value": float(p_c), "significant_at_0_05": bool(p_c < 0.05), "interpretation": "Device dependency on returns"})

    res_df = pd.DataFrame(results)
    res_df.to_csv(PROCESSED_DIR / "statistical_test_results.csv", index=False)
    logger.info("Statistical hypothesis tests complete.")
    return res_df

if __name__ == "__main__":
    run_statistical_tests()
