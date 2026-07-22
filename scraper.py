import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Educational scraping project - portfolio practice)"
}

# เก็บ URL ของแต่ละหมวดหมู่ไว้ใน dictionary (key = ชื่อหมวด, value = URL)
categories = {
    "iPhone": "https://www.bnn.in.th/en/p/apple/apple-iphone",
    "iPad": "https://www.bnn.in.th/en/p/apple/apple-ipad",
    "MacBook": "https://www.bnn.in.th/en/p/apple/apple-mac",
    "Apple Watch": "https://www.bnn.in.th/en/p/apple/apple-watch",
}

all_products = []

# วนลูปผ่านแต่ละหมวดหมู่
for category_name, url in categories.items():
    print(f"กำลังดึงข้อมูลหมวด: {category_name} ...")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select("a.product-item")

    print(f"  เจอสินค้า {len(products)} ชิ้นในหมวดนี้")

    for product in products:
        name = product.select_one("div.product-name")
        price = product.select_one("div.product-price")
        link = product.get("href")

        if name and price:
            price_text = price.text.strip()
            numbers = re.findall(r"[\d,]+", price_text)
            numbers_clean = [int(n.replace(",", "")) for n in numbers]

            price_min = numbers_clean[0] if len(numbers_clean) > 0 else None
            price_max = numbers_clean[1] if len(numbers_clean) > 1 else price_min

            product_data = {
                "category": category_name,       # ← เพิ่มคอลัมน์ใหม่ บอกว่าสินค้านี้อยู่หมวดไหน
                "name": name.text.strip(),
                "price_min": price_min,
                "price_max": price_max,
                "link": "https://www.bnn.in.th" + link
            }
            all_products.append(product_data)

    # หน่วงเวลา 2 วินาทีก่อนไปหมวดถัดไป (มารยาทในการ scraping ไม่ยิง request รัวๆ)
    time.sleep(2)

df = pd.DataFrame(all_products)
print("\nดึงข้อมูลสำเร็จทั้งหมด:", len(df), "ชิ้น จาก", len(categories), "หมวดหมู่")
print(df.groupby("category").size())  # นับจำนวนสินค้าต่อหมวด

df.to_csv("banana_apple_products.csv", index=False, encoding="utf-8-sig")
print("\nบันทึกไฟล์ banana_apple_products.csv สำเร็จ!")