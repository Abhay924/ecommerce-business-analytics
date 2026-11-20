import numpy as np
import pandas as pd
from config import PROCESSED_DIR, CHARTS_DIR

def test_clean_tables_integrity(clean_tables):
    assert clean_tables["customers"]["customer_id"].duplicated().sum() == 0
    assert clean_tables["orders"]["order_id"].duplicated().sum() == 0
    assert set(clean_tables["orders"]["customer_id"]).issubset(set(clean_tables["customers"]["customer_id"]))
    assert (clean_tables["products"]["unit_price"] >= clean_tables["products"]["unit_cost"]).all()

def test_analytics_outputs():
    rfm = pd.read_csv(PROCESSED_DIR / "rfm_segments.csv")
    assert set(rfm["r_score"].unique()).issubset({1, 2, 3, 4, 5})
    cohort = pd.read_csv(PROCESSED_DIR / "cohort_retention_matrix.csv", index_col=0)
    assert np.allclose(cohort["0"].dropna(), 100.0, atol=0.01)
    stats_df = pd.read_csv(PROCESSED_DIR / "statistical_test_results.csv")
    assert len(stats_df) == 3
    assert (CHARTS_DIR / "01_monthly_revenue_trend.png").exists()
