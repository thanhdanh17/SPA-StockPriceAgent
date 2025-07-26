# import json
# import pandas as pd

# # ----- CẤU HÌNH -----
# input_json_path = 'output\cafef_PVGAS.json'     # Đổi tên file JSON của bạn ở đây
# output_excel_path = 'pv_gas.xlsx'   # Tên file Excel đầu ra

# # ----- ĐỌC FILE JSON -----
# with open(input_json_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # ----- CHUYỂN DỮ LIỆU SANG DATAFRAME -----
# df = pd.DataFrame(data)

# # ----- LOẠI BỎ DỮ LIỆU TRÙNG LẶP THEO TIÊU ĐỀ -----
# df = df.drop_duplicates(subset='title')

# # ----- GHI RA FILE EXCEL -----
# df.to_excel(output_excel_path, index=False)

# print(f"✅ Đã xuất dữ liệu từ {input_json_path} sang {output_excel_path} (loại bỏ bài trùng theo title)")


import json
import pandas as pd
import re

def clean_text(text):
    """Loại bỏ ký tự không hợp lệ trong Excel."""
    if isinstance(text, str):
        return re.sub(r'[\x00-\x1F\x7F]', '', text)
    return text

# Đọc JSON
with open("data_GAS_19072025.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Tạo DataFrame
df = pd.DataFrame(data)

# Làm sạch toàn bộ nội dung trong từng cột
df = df.applymap(clean_text)

# Loại bỏ trùng lặp theo 'title'
df = df.drop_duplicates(subset="title")

# Xuất ra Excel
df.to_excel("data_GAS.xlsx", index=False)

print("✅ Xuất Excel thành công (đã làm sạch ký tự lỗi).")
