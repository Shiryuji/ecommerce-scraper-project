# BaNANA IT Product Data Pipeline

โปรเจกต์ Data Engineering ครบวงจร: ดึงข้อมูลสินค้าจากเว็บ e-commerce จริง (BaNANA IT),
ทำความสะอาดข้อมูล และเปิดให้เข้าถึงผ่าน REST API ของตัวเอง

## ทำไมถึงทำโปรเจกต์นี้

โปรเจกต์นี้จำลองงานจริงของตำแหน่ง Data Engineer / Data Operations โดยครอบคลุม
end-to-end pipeline ตั้งแต่ดึงข้อมูลดิบจนถึงเปิดให้ระบบอื่นเรียกใช้ได้จริง

## สถาปัตยกรรม (Architecture)
## Phase 1: Web Scraping

- ดึงข้อมูลสินค้าจาก [bnn.in.th](https://www.bnn.in.th) (BaNANA IT) หมวด Apple
  (iPhone, iPad, MacBook, Apple Watch)
- แกะข้อมูลด้วย BeautifulSoup จาก CSS selector ที่หาเองผ่าน browser inspection
- ทำความสะอาดข้อมูลราคาด้วย regular expression (แปลงจาก string เช่น "฿24,700 - ฿46,700"
  ให้เป็นตัวเลขที่วิเคราะห์ได้)
- ดึงข้อมูลอย่างมีความรับผิดชอบ: จำกัดจำนวนหมวดหมู่ ใส่ delay ระหว่าง request
  ใช้ User-Agent ที่ระบุวัตถุประสงค์ชัดเจน

**ไฟล์:** `scraper.py`
**ผลลัพธ์:** `banana_apple_products.csv` (87 รายการ, 4 หมวดหมู่)

## Phase 2: REST API

สร้าง API ด้วย FastAPI เปิดให้เข้าถึงข้อมูลที่ดึงมาผ่าน HTTP endpoints:

| Endpoint | คำอธิบาย |
|---|---|
| `GET /` | หน้าแรก |
| `GET /products` | ดึงสินค้าทั้งหมด |
| `GET /products/category/{category_name}` | กรองตามหมวดหมู่ (เช่น iPhone, iPad) |
| `GET /products/under/{max_price}` | กรองสินค้าที่ราคาเริ่มต้นไม่เกินที่กำหนด |

รองรับ error handling (คืน HTTP 404 พร้อมข้อความ เมื่อหาหมวดหมู่ไม่พบ)
มีเอกสาร API แบบ interactive อัตโนมัติที่ `/docs` (Swagger UI)

**ไฟล์:** `api.py`

## เทคโนโลยีที่ใช้

- **Python 3.14**
- **requests, BeautifulSoup4** — web scraping
- **pandas, re** — data cleaning & processing
- **FastAPI, Uvicorn** — REST API

## วิธีรันโปรเจกต์

```bash
# ติดตั้ง dependencies
pip install requests beautifulsoup4 pandas fastapi uvicorn

# รัน scraper เพื่อดึงข้อมูลใหม่
python3 scraper.py

# รัน API server
uvicorn api:app --reload

# เปิดดูเอกสาร API แบบ interactive
# http://127.0.0.1:8000/docs
```

## แผนพัฒนาต่อ (Roadmap)

- [ ] Data analysis: เปรียบเทียบราคาเฉลี่ยแต่ละหมวดหมู่ด้วย pandas
- [ ] เพิ่ม data quality checks (ตรวจสอบ null, ค่าผิดปกติ)
- [ ] โหลดข้อมูลเข้า cloud data warehouse (BigQuery)
- [ ] เพิ่ม scheduled scraping (รันอัตโนมัติทุกวัน)

## หมายเหตุสำคัญ

โปรเจกต์นี้ทำเพื่อการเรียนรู้และพอร์ตโฟลิโอส่วนตัวเท่านั้น (educational/personal use)
ไม่ใช้เพื่อการค้าหรือเผยแพร่ข้อมูลจำนวนมาก ดึงข้อมูลในปริมาณจำกัดและเว้นระยะเวลา
ระหว่าง request เพื่อไม่ให้เป็นภาระต่อเซิร์ฟเวอร์ปลายทาง