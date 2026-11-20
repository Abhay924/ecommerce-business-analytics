SET search_path TO core, public;

WITH rfm_raw AS (
    SELECT customer_id, ('2026-01-01'::DATE - MAX(order_date)::DATE) AS recency_days,
           COUNT(DISTINCT order_id) AS frequency, SUM(total_amount) AS monetary
    FROM orders WHERE order_status = 'Completed' GROUP BY customer_id
),
rfm_scores AS (
    SELECT customer_id, recency_days, frequency, ROUND(monetary, 2) AS monetary,
           NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
           NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
           NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
    FROM rfm_raw
)
SELECT customer_id, recency_days, frequency, monetary, r_score, f_score, m_score,
       CASE 
           WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
           WHEN r_score >= 3 AND f_score >= 4 THEN 'Loyal Customers'
           WHEN r_score >= 4 AND f_score BETWEEN 2 AND 3 THEN 'Potential Loyalists'
           WHEN r_score = 5 AND f_score = 1 THEN 'New Customers'
           WHEN r_score <= 2 AND f_score >= 4 THEN 'At Risk / Cannot Lose'
           WHEN r_score <= 2 AND f_score BETWEEN 2 AND 3 THEN 'Hibernating'
           ELSE 'Lost'
       END AS rfm_segment
FROM rfm_scores ORDER BY monetary DESC;
