from fastapi import FastAPI, HTTPException
import pandas as pd
import chromadb

app = FastAPI(title="BaNANA Apple Products API")
df = pd.read_csv("banana_apple_products.csv")

# เชื่อมต่อ Vector DB ที่สร้างไว้แล้วใน Phase 5
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="products")


@app.get("/")
def home():
    return {"message": "ยินดีต้อนรับสู่ BaNANA Apple Products API"}


@app.get("/products")
def get_all_products():
    return df.to_dict(orient="records")


@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    filtered = df[df["category"].str.lower() == category_name.lower()]
    if filtered.empty:
        raise HTTPException(status_code=404, detail=f"ไม่พบสินค้าในหมวด '{category_name}'")
    return filtered.to_dict(orient="records")


@app.get("/products/under/{max_price}")
def get_products_under_price(max_price: int):
    filtered = df[df["price_min"] <= max_price]
    return {
        "max_price": max_price,
        "count": len(filtered),
        "products": filtered.to_dict(orient="records")
    }


@app.get("/products/search")
def search_products(q: str, limit: int = 5):
    results = collection.query(query_texts=[q], n_results=limit)

    products = []
    for doc, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        products.append({
            "description": doc,
            "category": metadata["category"],
            "price_min": metadata["price_min"],
            "link": metadata["link"],
            "relevance_score": round(distance, 3)
        })

    return {"query": q, "results": products}