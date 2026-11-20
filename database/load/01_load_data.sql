SET search_path TO core, public;
TRUNCATE TABLE order_items, orders, marketing_campaigns, products, customers RESTART IDENTITY CASCADE;

COPY customers FROM '/var/lib/postgresql/data/processed/customers_clean.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');
COPY products FROM '/var/lib/postgresql/data/processed/products_clean.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');
COPY marketing_campaigns FROM '/var/lib/postgresql/data/processed/campaigns_clean.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');
COPY orders FROM '/var/lib/postgresql/data/processed/orders_clean.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');
COPY order_items FROM '/var/lib/postgresql/data/processed/order_items_clean.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');

ANALYZE customers;
ANALYZE products;
ANALYZE marketing_campaigns;
ANALYZE orders;
ANALYZE order_items;
