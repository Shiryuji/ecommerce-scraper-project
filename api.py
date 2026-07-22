from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI(title="BaNANA Apple Products API")
df = pd.read_csv("banana_apple_products.csv")

@app.get("/")
def home():
    return {"message": "ยินดีต้อนรับสู่ BaNANA Apple Products API"}

@app.get("/products")
def get_all_products():
    return df.to_dict(orient="records")

# endpoint ใหม่: กรองสินค้าตามหมวดหมู่ เช่น /products/category/iPhone
@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    # กรองเฉพาะแถวที่ column "category" ตรงกับที่ระบุ (ไม่สนตัวพิมพ์เล็ก-ใหญ่)
    filtered = df[df["category"].str.lower() == category_name.lower()]

    if filtered.empty:
        # ถ้าไม่เจอเลย ส่ง error 404 กลับไปพร้อมข้อความอธิบาย
        raise HTTPException(status_code=404, detail=f"ไม่พบสินค้าในหมวด '{category_name}'")

    return filtered.to_dict(orient="records")

# endpoint ใหม่: หาสินค้าที่ราคาไม่เกินที่กำหนด เช่น /products/under/30000
@app.get("/products/under/{max_price}")
def get_products_under_price(max_price: int):
    filtered = df[df["price_min"] <= max_price]
    return {
        "max_price": max_price,
        "count": len(filtered),
        "products": filtered.to_dict(orient="records")
    }