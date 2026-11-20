# Power BI Integration Guide
1. Connect Power BI Desktop to PostgreSQL (`ecommerce_analytics`) or import CSVs from `data/processed/`.
2. Link fact tables (`orders`, `order_items`) to dimension tables (`customers`, `products`, `marketing_campaigns`).
3. Copy formulas from `dax_measures.md` into a dedicated `_Measures` table.
