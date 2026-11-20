SET search_path TO core, public;

WITH customer_lifetime AS (
    SELECT 
        c.customer_id, c.country, c.acquisition_channel,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COALESCE(SUM(o.total_amount), 0) AS lifetime_spend
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status = 'Completed'
    GROUP BY c.customer_id, c.country, c.acquisition_channel
)
SELECT 
    country, acquisition_channel,
    COUNT(customer_id) AS total_customers,
    ROUND(100.0 * COUNT(CASE WHEN total_orders >= 2 THEN 1 END) / NULLIF(COUNT(CASE WHEN total_orders >= 1 THEN 1 END), 0), 2) AS repeat_purchase_rate_pct,
    ROUND(AVG(lifetime_spend), 2) AS avg_clv
FROM customer_lifetime
GROUP BY country, acquisition_channel
ORDER BY avg_clv DESC;
