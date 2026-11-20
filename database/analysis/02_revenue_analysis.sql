SET search_path TO core, public;

WITH monthly_financials AS (
    SELECT 
        DATE_TRUNC('month', o.order_date)::DATE AS order_month,
        COUNT(DISTINCT o.order_id) AS completed_orders,
        SUM(o.total_amount) AS net_revenue,
        SUM(oi.line_margin) AS gross_profit
    FROM orders o
    JOIN (SELECT order_id, SUM(line_margin) AS line_margin FROM order_items GROUP BY order_id) oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY 1
)
SELECT 
    order_month,
    completed_orders,
    ROUND(net_revenue, 2) AS net_revenue,
    ROUND(gross_profit, 2) AS gross_profit,
    ROUND(100.0 * gross_profit / NULLIF(net_revenue, 0), 2) AS gross_margin_pct,
    ROUND(100.0 * (net_revenue - LAG(net_revenue) OVER (ORDER BY order_month)) / NULLIF(LAG(net_revenue) OVER (ORDER BY order_month), 0), 2) AS mom_growth_pct
FROM monthly_financials
ORDER BY order_month;
