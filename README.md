# E-Commerce Business Analytics Suite
End-to-end SQL, Python, Excel, and Power BI analytics pipeline for e-commerce operations.

## Quickstart
```bash
pip install -r requirements.txt
python python/01_generate_dataset.py
python python/02_data_quality_check.py
python python/03_data_cleaning.py
python python/04_eda.py
python python/05_customer_analysis.py
python python/06_product_analysis.py
python python/07_rfm_segmentation.py
python python/08_cohort_analysis.py
python python/09_marketing_analysis.py
python python/10_statistical_analysis.py
python build_notebooks_and_excel.py
pytest tests/ -v
```
