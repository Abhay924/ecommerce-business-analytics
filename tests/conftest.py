import sys
from pathlib import Path
import importlib
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
PYTHON_DIR = ROOT_DIR / "python"
if str(PYTHON_DIR) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIR))

from utils import load_clean_tables

@pytest.fixture(scope="session", autouse=True)
def execute_pipeline_once():
    for mod_name in [
        "01_generate_dataset", "02_data_quality_check", "03_data_cleaning",
        "04_eda", "05_customer_analysis", "06_product_analysis",
        "07_rfm_segmentation", "08_cohort_analysis", "09_marketing_analysis",
        "10_statistical_analysis"
    ]:
        mod = importlib.import_module(mod_name)
        for fn in ["generate_datasets", "run_quality_checks", "clean_all_datasets", "run_eda",
                   "run_customer_analysis", "run_product_analysis", "run_rfm_segmentation",
                   "run_cohort_analysis", "run_marketing_analysis", "run_statistical_tests"]:
            if hasattr(mod, fn):
                getattr(mod, fn)()

@pytest.fixture(scope="session")
def clean_tables():
    return load_clean_tables()
