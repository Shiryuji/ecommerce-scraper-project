import sqlite3
import pandas as pd

conn = sqlite3.connect("products.db")

print("=" * 60)
print("Query 1: ราคาเฉลี่ย/สูงสุด/ต่ำสุด แยกตามหมวดหมู่ (GROUP BY)")
print("=" * 60)
query1 = """
SELECT
    category,
    COUNT(*) AS total_products,
    ROUND(AVG(price_min), 0) AS avg_price,
    MAX(price_min) AS max_price,
    MIN(price_min) AS min_price
FROM products
GROUP BY category
ORDER BY avg_price DESC;
"""
print(pd.read_sql_query(query1, conn))

print()
print("=" * 60)
print("Query 2: สินค้า Top 3 ที่แพงที่สุดในแต่ละหมวด (Window Function)")
print("=" * 60)
query2 = """
SELECT category, name, price_min, rank
FROM (
    SELECT
        category,
        name,
        price_min,
        RANK() OVER (PARTITION BY category ORDER BY price_min DESC) AS rank
    FROM products
)
WHERE rank <= 3
ORDER BY category, rank;
"""
print(pd.read_sql_query(query2, conn))

print()
print("=" * 60)
print("Query 3: สินค้าที่ราคาสูงกว่าค่าเฉลี่ยของหมวดตัวเอง (Subquery)")
print("=" * 60)
query3 = """
SELECT p.category, p.name, p.price_min
FROM products p
WHERE p.price_min > (
    SELECT AVG(price_min)
    FROM products
    WHERE category = p.category
)
ORDER BY p.category, p.price_min DESC;
"""
print(pd.read_sql_query(query3, conn))

conn.close()