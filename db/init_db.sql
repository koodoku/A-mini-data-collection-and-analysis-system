-- Добавьте эту секцию в самое начало файла
-- Создаем базу данных для Redash, так как postgres создает только ecommerce_db по умолчанию
CREATE DATABASE redash_db OWNER "user";

-- Далее ваш старый код для ecommerce_db
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    city VARCHAR(100) NOT NULL,
    total_revenue NUMERIC(10, 2) GENERATED ALWAYS AS (price * quantity) STORED
);