# Power BI DAX Measures
```dax
Net Revenue = CALCULATE(SUM(orders[total_amount]), orders[order_status] = "Completed")
Gross Margin ($) = CALCULATE(SUM(order_items[line_margin]), orders[order_status] = "Completed")
Gross Margin (%) = DIVIDE([Gross Margin ($)], [Net Revenue], 0)
Average Order Value (AOV) = DIVIDE([Net Revenue], CALCULATE(DISTINCTCOUNT(orders[order_id]), orders[order_status] = "Completed"), 0)
Campaign ROAS = DIVIDE([Net Revenue], SUM(marketing_campaigns[budget]), 0)
```
