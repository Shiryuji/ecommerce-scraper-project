import pandas as pd
import matplotlib.pyplot as plt


# โหลดข้อมูลที่ดึงมาจาก Phase 1
df = pd.read_csv("banana_apple_products.csv")

print("=" * 50)
print("ภาพรวมข้อมูล")
print("=" * 50)
print(f"จำนวนสินค้าทั้งหมด: {len(df)} ชิ้น")
print(f"จำนวนหมวดหมู่: {df['category'].nunique()} หมวด")
print()

# 1. เปรียบเทียบราคาเฉลี่ยแต่ละหมวดหมู่
print("=" * 50)
print("ราคาเฉลี่ย (price_min) แยกตามหมวดหมู่")
print("=" * 50)
avg_price_by_category = df.groupby("category")["price_min"].mean().sort_values(ascending=False)
print(avg_price_by_category.round(0))
print()

# 2. หาสินค้าที่แพงที่สุดและถูกที่สุดในแต่ละหมวด
print("=" * 50)
print("สินค้าแพงที่สุด vs ถูกที่สุด แยกตามหมวดหมู่")
print("=" * 50)
for category in df["category"].unique():
    category_df = df[df["category"] == category]

    most_expensive = category_df.loc[category_df["price_min"].idxmax()]
    cheapest = category_df.loc[category_df["price_min"].idxmin()]

    print(f"\n[{category}]")
    print(f"  แพงสุด: {most_expensive['name']} — ฿{most_expensive['price_min']:,.0f}")
    print(f"  ถูกสุด: {cheapest['name']} — ฿{cheapest['price_min']:,.0f}")

print()
print("=" * 50)
print("สรุปสถิติราคาทั้งหมด (price_min)")
print("=" * 50)
print(df["price_min"].describe().round(0))

plt.figure(figsize=(8, 5))
avg_price_by_category.plot(kind="bar", color="#4A90D9")
plt.title("Average Price by Category - Apple Products (BaNANA IT)")
plt.xlabel("Category")
plt.ylabel("Average Price (THB)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("price_by_category.png", dpi=150)
print("\nบันทึกกราฟ price_by_category.png สำเร็จ!")