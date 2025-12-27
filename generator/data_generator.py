import psycopg2
import time
import random
import numpy as np
import os

DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_NAME = os.environ.get('POSTGRES_DB', 'ecommerce_db')
DB_USER = os.environ.get('POSTGRES_USER', 'user')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'password')

CATEGORIES = ['Electronics', 'Books', 'Apparel', 'Home & Garden', 'Beauty']
CITIES = ['Moscow', 'St. Petersburg', 'Kazan', 'Novosibirsk', 'Vladivostok']

PRODUCT_MAP = {
    'Electronics': [('Laptop', 800.00), ('Smartphone', 500.00), ('Headphones', 50.00)],
    'Books': [('Novel', 15.00), ('Textbook', 50.00), ('Cookbook', 25.00)],
    'Apparel': [('T-Shirt', 20.00), ('Jeans', 60.00), ('Jacket', 120.00)],
    'Home & Garden': [('Blender', 70.00), ('Vase', 30.00), ('Drill', 150.00)],
    'Beauty': [('Perfume', 80.00), ('Cream', 45.00), ('Shampoo', 10.00)],
}

def connect_to_db():
    conn = None
    max_retries = 10
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            print(f"Connecting to DB attempt {attempt + 1}/{max_retries}...")
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            print("Successfully connected to the database!")
            return conn
        except psycopg2.OperationalError as e:
            print(f"DB connection failed: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    
    print("FATAL: Could not connect to the database after multiple retries.")
    return None

def generate_order_data():
    category = random.choice(CATEGORIES)
    city = random.choice(CITIES)
    
    product_name, base_price = random.choice(PRODUCT_MAP[category])
    price = round(base_price + np.random.normal(0, 0.05 * base_price), 2)
    quantity = int(np.random.poisson(1.5)) + 1 
    
    return product_name, category, price, quantity, city

def insert_data(conn, cursor, data):
    product_name, category, price, quantity, city = data 
    
    insert_query = """
    INSERT INTO orders (product_name, category, price, quantity, city)
    VALUES (%s, %s, %s, %s, %s);
    """
    
    try:
        cursor.execute(insert_query, (product_name, category, price, quantity, city))
        conn.commit()
        print(f"Inserted: {product_name} ({category}) in {city}. Price: {price}, Qty: {quantity}")
    except Exception as e:
        print(f"Error during insertion: {e}")
        conn.rollback()

def main():
    conn = connect_to_db()
    if not conn:
        return

    cursor = conn.cursor()
    
    print("Starting data generation loop...")
    while True:
        order_data = generate_order_data()
        insert_data(conn, cursor, order_data)
        
        time.sleep(1) 

if __name__ == "__main__":
    main()