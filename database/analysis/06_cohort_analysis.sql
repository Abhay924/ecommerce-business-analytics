SET search_path TO core, public;

WITH first_purchase AS (
    SELECT customer_id, DATE_TRUNC('month', MIN(order_date))::DATE AS cohort_month
    FROM orders WHERE order_status = 'Completed' GROUP BY customer_id
),
cohort_activity AS (
    SELECT 
        fp.cohort_month,
        (EXTRACT(YEAR FROM o.order_date) - EXTRACT(YEAR FROM fp.cohort_month)) * 12 +
        (EXTRACT(MONTH FROM o.order_date) - EXTRACT(MONTH FROM fp.cohort_month)) AS month_number,
        COUNT(DISTINCT o.customer_id) AS active_customers
    FROM orders o
    JOIN first_purchase fp ON o.customer_id = fp.customer_id
    WHERE o.order_status = 'Completed'
    GROUP BY fp.cohort_month, month_number
),
cohort_size AS (
    SELECT cohort_month, active_customers AS initial_customers FROM cohort_activity WHERE month_number = 0
)
SELECT 
    ca.cohort_month, cs.initial_customers, ca.month_number, ca.active_customers,
    ROUND(100.0 * ca.active_customers / cs.initial_customers, 2) AS retention_rate_pct
FROM cohort_activity ca
JOIN cohort_size cs ON ca.cohort_month = cs.cohort_month
WHERE ca.month_number BETWEEN 0 AND 12
ORDER BY ca.cohort_month, ca.month_number;
