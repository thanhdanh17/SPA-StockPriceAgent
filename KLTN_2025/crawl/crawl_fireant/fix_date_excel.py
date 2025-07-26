# import pandas as pd
# from datetime import datetime

# def fix_year_for_reverse_chronological_dates(date_strings, date_format="%d-%m-%Y - %I:%M %p", start_year=None):
#     fixed_dates = []
#     prev_month = None
#     current_year = start_year or datetime.now().year

#     for i, date_str in enumerate(date_strings):
#         try:
#             dt = datetime.strptime(date_str, date_format)
#         except Exception as e:
#             print(f"⚠️ Lỗi dòng {i}: {date_str} → {e}")
#             fixed_dates.append(None)
#             continue

#         if i == 0:
#             prev_month = dt.month
#             dt = dt.replace(year=current_year)
#         else:
#             if dt.month > prev_month:
#                 current_year -= 1
#             prev_month = dt.month
#             dt = dt.replace(year=current_year)

#         fixed_dates.append(dt.strftime(date_format))

#     return fixed_dates

# # ✅ Bước 1: Đọc file Excel gốc
# df = pd.read_excel("FPT\data_FPT_09072025_fireant.xlsx", engine="openpyxl")

# # ✅ Bước 2: Lấy cột H - datetime
# date_series = df["datetime"].dropna().astype(str)
# date_strings = date_series.tolist()

# # ✅ Bước 3: Fix năm với năm đầu tiên là 2025
# fixed_dates = fix_year_for_reverse_chronological_dates(date_strings, start_year=2025)

# # ✅ Bước 4: Gán vào cột I - datetime_fixed
# df.loc[date_series.index, "datetime_fixed"] = fixed_dates

# # ✅ Bước 5: Ghi ra file mới
# df.to_excel("output_fixed_final.xlsx", index=False)

# print("✅ Đã hoàn tất! File lưu tại: output_fixed_final.xlsx")


# -----------------------------------------------------VIET-----------------------------------------------------------------


import pandas as pd
from datetime import datetime

INPUT_FILE_PATH = 'data_GAS.xlsx'

try:
    df = pd.read_excel(INPUT_FILE_PATH)

    if 'datetime' not in df.columns or 'fixed' not in df.columns:
        raise ValueError("Cần có đủ cột 'datetime' và 'fixed' trong file.")

    # --- Bắt đầu xử lý ---
    for i in range(1, len(df)):
        curr_raw = df.loc[i, 'datetime']
        prev_raw = df.loc[i - 1, 'datetime']

        # ✅ Bỏ qua nếu là NaN hoặc không phải chuỗi
        if pd.isna(curr_raw) or pd.isna(prev_raw):
            continue
        if not isinstance(curr_raw, str) or not isinstance(prev_raw, str):
            continue

        try:
            curr = datetime.strptime(curr_raw.strip(), "%d-%m-%Y - %I:%M %p")
            prev = datetime.strptime(prev_raw.strip(), "%d-%m-%Y - %I:%M %p")

            # Kiểm tra chuyển năm (từ tháng 01 → 12)
            if curr.month == 12 and prev.month == 1:
                new_year = prev.year - 1
            else:
                new_year = prev.year

            # Cập nhật lại cột datetime với năm mới
            curr = curr.replace(year=new_year)
            df.loc[i, 'datetime'] = curr.strftime("%d-%m-%Y - %I:%M %p")

        except Exception as e:
            print(f"⚠️ Lỗi tại dòng {i}: {e}")

    # --- Lưu kết quả ---
    df.to_excel(INPUT_FILE_PATH, index=False)
    print("✅ Xử lý xong và lưu lại file thành công!")

except FileNotFoundError:
    print(f"❌ Không tìm thấy file: {INPUT_FILE_PATH}")
except Exception as e:
    print(f"⚠️ Đã xảy ra lỗi: {e}")
