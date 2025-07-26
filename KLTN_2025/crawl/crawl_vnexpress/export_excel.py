import json
import pandas as pd

# Đọc file JSON
with open('vnexpress_ai_articles.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Tạo DataFrame
df = pd.DataFrame(data)

# ✅ Loại bỏ các dòng trùng lặp dựa trên tất cả cột (hoặc chỉ cột 'title' nếu bạn muốn)
df.drop_duplicates(inplace=True)  # loại theo tất cả các cột
# df.drop_duplicates(subset='title', inplace=True)  # chỉ loại theo cột 'title'

# Ghi ra file Excel
df.to_excel('news_data_dedup.xlsx', index=False, engine='openpyxl')

print("✅ Đã loại bỏ trùng lặp và xuất ra file news_data_dedup.xlsx")
