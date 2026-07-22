import sqlite3
import pandas as pd

# โหลดข้อมูลจาก CSV ที่มีอยู่แล้ว
df = pd.read_csv("banana_apple_products.csv")

# เชื่อมต่อ (หรือสร้างใหม่ถ้ายังไม่มี) ไฟล์ database ชื่อ products.db
conn = sqlite3.connect("products.db")

# เขียนข้อมูลจาก DataFrame ลงในตารางชื่อ "products"
# if_exists="replace" คือถ้ามีตารางนี้อยู่แล้ว ให้ลบทิ้งแล้วสร้างใหม่ (สำหรับตอน dev/ทดสอบ)
df.to_sql("products", conn, if_exists="replace", index=False)

print(f"โหลดข้อมูล {len(df)} แถวเข้า database สำเร็จ!")

# ทดสอบ query ง่ายๆ เพื่อเช็คว่าข้อมูลเข้าไปจริง
result = conn.execute("SELECT COUNT(*) FROM products").fetchone()
print(f"จำนวนแถวใน table products: {result[0]}")

conn.close()