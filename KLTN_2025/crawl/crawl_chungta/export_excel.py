import json
import pandas as pd

# Đường dẫn đến file JSON đầu vào
json_file_path = 'chungta.json'  # Đổi tên nếu cần

# Đường dẫn đến file Excel đầu ra
excel_file_path = 'data_chungta_kinhdoanh.xlsx'

# Đọc dữ liệu từ file JSON
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Chuyển đổi thành DataFrame
df = pd.DataFrame(data)

# Ghi ra file Excel
df.to_excel(excel_file_path, index=False, engine='openpyxl')

print(f"✅ Đã xuất dữ liệu ra file Excel: {excel_file_path}")
