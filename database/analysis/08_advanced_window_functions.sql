SET search_path TO core, public;

WITH ranked_products AS (
    SELECT p.category, p.product_id, p.product_name, ROUND(SUM(oi.line_margin), 2) AS total_margin,
           DENSE_RANK() OVER (PARTITION BY p.category ORDER BY SUM(oi.line_margin) DESC) AS category_rank
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY p.category, p.product_id, p.product_name
)
SELECT * FROM ranked_products WHERE category_rank <= 3 ORDER BY category, category_rank;
