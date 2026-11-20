from pathlib import Path
import nbformat as nbf
import pandas as pd

ROOT = Path(__file__).resolve().parent
NOTEBOOKS_DIR = ROOT / "notebooks"
PROCESSED_DIR = ROOT / "data" / "processed"
EXCEL_FILE = ROOT / "excel" / "ecommerce_analysis.xlsx"

NOTEBOOK_SPECS = {
    "01_data_cleaning_and_eda.ipynb": ("Data Cleaning & EDA", "python/03_data_cleaning.py", "python/04_eda.py"),
    "02_customer_analysis.ipynb": ("Customer CLV Analysis", "python/05_customer_analysis.py", None),
    "03_product_analysis.ipynb": ("Product & Category Profitability", "python/06_product_analysis.py", None),
    "04_rfm_segmentation.ipynb": ("RFM Customer Segmentation", "python/07_rfm_segmentation.py", None),
    "05_cohort_analysis.ipynb": ("Monthly Cohort Retention", "python/08_cohort_analysis.py", None),
    "06_statistical_analysis.ipynb": ("Statistical Hypothesis Testing", "python/10_statistical_analysis.py", None),
}

def main():
    for nb_name, (title, s1, s2) in NOTEBOOK_SPECS.items():
        nb = nbf.v4.new_notebook()
        cells = [nbf.v4.new_markdown_cell(f"# {title}"), nbf.v4.new_code_cell("import sys; from pathlib import Path; sys.path.append(str(Path.cwd().parent / 'python'))")]
        for scr in [s1, s2]:
            if scr and (ROOT / scr).exists():
                cells.append(nbf.v4.new_code_cell((ROOT / scr).read_text(encoding="utf-8")))
        nb["cells"] = cells
        with open(NOTEBOOKS_DIR / nb_name, "w", encoding="utf-8") as f:
            nbf.write(nb, f)

    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
        for csv_name, sheet_name in [
            ("category_performance.csv", "Category_Performance"),
            ("rfm_segments.csv", "RFM_Segments"),
            ("cohort_retention_matrix.csv", "Cohort_Retention"),
            ("campaign_performance.csv", "Marketing_ROAS"),
            ("statistical_test_results.csv", "Statistical_Tests"),
        ]:
            csv_path = PROCESSED_DIR / csv_name
            if csv_path.exists():
                pd.read_csv(csv_path).to_excel(writer, sheet_name=sheet_name, index=False)
    print("Successfully built 6 Jupyter Notebooks and ecommerce_analysis.xlsx!")

if __name__ == "__main__":
    main()
