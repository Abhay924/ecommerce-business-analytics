SET search_path TO core, public;

WITH product_performance AS (
    SELECT 
        p.product_id, p.product_name, p.category,
        SUM(CASE WHEN o.order_status = 'Completed' THEN oi.quantity ELSE 0 END) AS units_sold,
        SUM(CASE WHEN o.order_status = 'Completed' THEN oi.line_total ELSE 0 END) AS net_sales,
        SUM(CASE WHEN o.order_status = 'Completed' THEN oi.line_margin ELSE 0 END) AS gross_margin
    FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    LEFT JOIN orders o ON oi.order_id = o.order_id
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT 
    product_id, product_name, category, units_sold,
    ROUND(net_sales, 2) AS net_sales,
    ROUND(gross_margin, 2) AS gross_margin,
    ROUND(100.0 * SUM(net_sales) OVER (ORDER BY net_sales DESC) / NULLIF(SUM(net_sales) OVER (), 0), 2) AS cumulative_revenue_share_pct
FROM product_performance
ORDER BY net_sales DESC;
