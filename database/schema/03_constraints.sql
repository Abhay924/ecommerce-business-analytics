SET search_path TO core, public;

ALTER TABLE orders ADD CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT;
ALTER TABLE orders ADD CONSTRAINT fk_orders_campaign FOREIGN KEY (campaign_id) REFERENCES marketing_campaigns(campaign_id) ON DELETE SET NULL;
ALTER TABLE order_items ADD CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE;
ALTER TABLE order_items ADD CONSTRAINT fk_order_items_product FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT;

ALTER TABLE customers ADD CONSTRAINT chk_customer_age CHECK (age BETWEEN 16 AND 110);
ALTER TABLE products ADD CONSTRAINT chk_product_prices CHECK (unit_price >= unit_cost AND unit_cost >= 0),
                     ADD CONSTRAINT chk_product_rating CHECK (rating BETWEEN 1.00 AND 5.00);
ALTER TABLE order_items ADD CONSTRAINT chk_item_quantity CHECK (quantity > 0);

CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_customers_country_channel ON customers(country, acquisition_channel);
CREATE INDEX idx_products_category ON products(category, subcategory);
