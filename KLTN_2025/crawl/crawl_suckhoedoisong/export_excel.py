import pandas as pd
import json

# Đọc dữ liệu từ file JSON (hoặc biến list nếu đã có sẵn trong Python)
with open("crawl_news\suckhoedoisong_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# articles phải có cấu trúc như:
# [
#   {
#       "url": "...",
#       "title": "...",
#       "date": "...",
#       "content": "...",
#       "category": "...",
#       "industry": "...",     # bạn tự gán hoặc model gán
#       "sentiment": "..."     # bạn tự gán hoặc model gán
#   },
#   ...
# ]

# Chuyển thành DataFrame
df = pd.DataFrame(articles)

# Lưu thành file Excel
df.to_excel("articles_labeled.xlsx", index=False)

print("✅ Đã xuất file Excel thành công với", len(df), "bài viết.")
