# E-Commerce Data Dictionary
- **customers**: `customer_id` (PK), `first_name`, `last_name`, `email`, `gender`, `age`, `city`, `state`, `country`, `acquisition_channel`, `signup_date`, `is_active`
- **products**: `product_id` (PK), `product_name`, `category`, `subcategory`, `brand`, `unit_cost`, `unit_price`, `stock_quantity`, `rating`
- **marketing_campaigns**: `campaign_id` (PK), `campaign_name`, `channel`, `budget`, `impressions`, `clicks`, `conversions`, `start_date`, `end_date`
- **orders**: `order_id` (PK), `customer_id` (FK), `campaign_id` (FK), `order_date`, `order_status`, `payment_method`, `device_type`, `shipping_cost`, `discount_amount`, `total_amount`
- **order_items**: `order_item_id` (PK), `order_id` (FK), `product_id` (FK), `quantity`, `unit_price`, `unit_cost`, `discount_pct`, `line_total`, `line_margin`
