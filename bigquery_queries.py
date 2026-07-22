from google.cloud import bigquery

PROJECT_ID = "banana-data-pipeline"
client = bigquery.Client(project=PROJECT_ID)

query = """
SELECT
    category,
    COUNT(*) AS total_products,
    ROUND(AVG(price_min), 0) AS avg_price,
    MAX(price_min) AS max_price,
    MIN(price_min) AS min_price
FROM `banana-data-pipeline.banana_products.apple_products`
GROUP BY category
ORDER BY avg_price DESC
"""

# รัน query แล้วแปลงผลลัพธ์เป็น DataFrame ทันที
result_df = client.query(query).to_dataframe()

print("ผลลัพธ์จาก BigQuery:")
print(result_df)