SET search_path TO core, public;

SELECT 
    mc.campaign_id, mc.campaign_name, mc.channel, mc.budget,
    ROUND(100.0 * mc.clicks / NULLIF(mc.impressions, 0), 2) AS ctr_pct,
    COUNT(DISTINCT o.order_id) AS attributed_orders,
    ROUND(SUM(o.total_amount), 2) AS attributed_revenue,
    ROUND(SUM(o.total_amount) / NULLIF(mc.budget, 0), 2) AS roas,
    ROUND(mc.budget / NULLIF(COUNT(DISTINCT o.customer_id), 0), 2) AS cac
FROM marketing_campaigns mc
LEFT JOIN orders o ON mc.campaign_id = o.campaign_id AND o.order_status = 'Completed'
GROUP BY mc.campaign_id, mc.campaign_name, mc.channel, mc.budget, mc.impressions, mc.clicks
ORDER BY roas DESC NULLS LAST;
