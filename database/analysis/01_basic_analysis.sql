SET search_path TO core, public;

SELECT 
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS active_customers,
    ROUND(SUM(CASE WHEN o.order_status = 'Completed' THEN o.total_amount ELSE 0 END), 2) AS net_revenue,
    ROUND(AVG(CASE WHEN o.order_status = 'Completed' THEN o.total_amount END), 2) AS avg_order_value,
    ROUND(SUM(CASE WHEN o.order_status = 'Completed' THEN oi.line_margin ELSE 0 END), 2) AS total_gross_margin,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN o.order_status = 'Returned' THEN o.order_id END) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS return_rate_pct
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id;
