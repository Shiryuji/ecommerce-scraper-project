import chromadb
import pandas as pd

# โหลดข้อมูลสินค้า
df = pd.read_csv("banana_apple_products.csv")

# สร้าง Chroma client แบบเก็บข้อมูลลงไฟล์ในเครื่อง (persistent)
client = chromadb.PersistentClient(path="./chroma_db")

# สร้าง (หรือเปิด) collection ชื่อ "products"
# get_or_create_collection = ถ้ามีอยู่แล้วให้เปิดใช้ ถ้ายังไม่มีให้สร้างใหม่
collection = client.get_or_create_collection(name="products")

# เตรียมข้อมูลสำหรับใส่เข้า Vector DB
# documents = ข้อความที่จะถูกแปลงเป็นเวกเตอร์ (ใช้ชื่อสินค้า + หมวดหมู่ + ราคา)
documents = []
metadatas = []
ids = []

for idx, row in df.iterrows():
    text = f"{row['name']} - Category: {row['category']} - Price: {row['price_min']} THB"
    documents.append(text)
    metadatas.append({
        "category": row["category"],
        "price_min": int(row["price_min"]),
        "link": row["link"]
    })
    ids.append(f"product_{idx}")

# ใส่ข้อมูลเข้า Vector DB ทีเดียวทั้งหมด
# ChromaDB จะแปลง documents เป็นเวกเตอร์ให้อัตโนมัติ (ใช้ embedding model ในตัว)
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print(f"สร้าง Vector DB สำเร็จ! ใส่ข้อมูล {len(documents)} สินค้าเข้าไปแล้ว")

def search_products(query_text, n_results=5):
    """ค้นหาสินค้าด้วยข้อความอิสระ (natural language)"""
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )

    print(f"\nค้นหา: '{query_text}'")
    print("-" * 60)

    # results เป็น dictionary ที่มี key "documents", "metadatas", "distances"
    # ทั้งหมดเป็น list ซ้อน list (เพราะ query ได้หลายคำถามพร้อมกัน เราถามแค่ 1 คำถาม เลยดู index [0])
    docs = results["documents"][0]
    distances = results["distances"][0]

    for doc, distance in zip(docs, distances):
        # distance ยิ่งน้อย = ยิ่งใกล้เคียงกับคำค้นหามากขึ้น
        print(f"  [{distance:.3f}] {doc}")

# ทดสอบค้นหาด้วยประโยคธรรมชาติ ไม่ใช่ keyword ตรงๆ
search_products("laptop for video editing and creative work")
search_products("cheap smartwatch under 15000 baht")
search_products("powerful computer for professional use")