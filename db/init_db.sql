DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    -- Уникальный идентификатор заказа
    id SERIAL PRIMARY KEY,
    
    -- Время создания записи 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Поля, специфичные для интернет-магазина:
    product_name VARCHAR(255) NOT NULL,    -- Товар
    category VARCHAR(100) NOT NULL,        -- Категория
    price NUMERIC(10, 2) NOT NULL,         -- Цена
    quantity INTEGER NOT NULL,             -- Количество
    city VARCHAR(100) NOT NULL,            -- Город
    
    -- Расчетное поле: общая стоимость заказа
    total_revenue NUMERIC(10, 2) GENERATED ALWAYS AS (price * quantity) STORED
);