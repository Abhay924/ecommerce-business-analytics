DROP DATABASE IF EXISTS ecommerce_analytics;
CREATE DATABASE ecommerce_analytics WITH OWNER = postgres ENCODING = 'UTF8';
CREATE SCHEMA IF NOT EXISTS core;
SET search_path TO core, public;
