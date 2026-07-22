import pandas as pd
from google.cloud import bigquery

# ตั้งชื่อ project ตรงกับที่สร้างไว้ใน GCP
PROJECT_ID = "banana-data-pipeline"
DATASET_ID = "banana_products"       # เหมือน "โฟลเดอร์" เก็บกลุ่มตาราง
TABLE_ID = "apple_products"          # ชื่อตารางที่จะสร้าง

# โหลดข้อมูลจาก CSV เดิม
df = pd.read_csv("banana_apple_products.csv")

# สร้าง client เชื่อมต่อ BigQuery
client = bigquery.Client(project=PROJECT_ID)

# สร้าง dataset ถ้ายังไม่มี (เหมือนสร้างโฟลเดอร์ก่อนใส่ไฟล์)
dataset_ref = bigquery.Dataset(f"{PROJECT_ID}.{DATASET_ID}")
dataset_ref.location = "asia-southeast1"  # เลือก region สิงคโปร์ (ใกล้ไทยที่สุด)

try:
    client.create_dataset(dataset_ref, exists_ok=True)
    print(f"Dataset '{DATASET_ID}' พร้อมใช้งาน")
except Exception as e:
    print(f"Error creating dataset: {e}")

# กำหนดปลายทางแบบเต็ม (project.dataset.table)
table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

# ส่งข้อมูลจาก DataFrame ขึ้น BigQuery
job = client.load_table_from_dataframe(df, table_ref)
job.result()  # รอจนกว่างานจะเสร็จ

print(f"อัปโหลดข้อมูล {len(df)} แถวขึ้น BigQuery สำเร็จ!")
print(f"ตาราง: {table_ref}")