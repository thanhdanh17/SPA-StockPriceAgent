from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests
import json

# ⚙️ Cấu hình Selenium Chrome
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")  # Bỏ comment nếu muốn chạy ẩn

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://chungta.vn/kinh-doanh")
wait = WebDriverWait(driver, 10)

# 🔁 Bấm "Xem thêm" để tải thêm bài
for _ in range(1000):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        button = wait.until(EC.element_to_be_clickable((By.ID, "load_more_redesign")))
        button.click()
        time.sleep(4)
    except:
        print("Không thể click hoặc đã hết bài.")
        break

# 📄 Lấy HTML sau khi đã bấm hết bài
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

articles = soup.select("h3.title-news a")
print(f"Tìm thấy {len(articles)} bài viết.")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

results = []

# 🔍 Truy cập từng bài viết
for a in articles:
    title_preview = a.get_text(strip=True)
    link = "https://chungta.vn" + a.get("href")

    try:
        res = requests.get(link, headers=headers, timeout=10)
        article_soup = BeautifulSoup(res.text, "html.parser")

        time.sleep(2)

        # Tiêu đề chi tiết
        title = article_soup.select_one("h1.title-detail")
        title = title.get_text(strip=True) if title else title_preview

        # Thời gian đăng
        date = article_soup.select_one("span.time")
        date = date.get_text(strip=True) if date else "Không rõ ngày"

        # Mô tả
        lead = article_soup.select_one("p.lead-detail")
        lead_text = lead.get_text(strip=True) if lead else ""

        # Nội dung chính
        body = article_soup.select_one("article.fck_detail.width_common")
        content = body.get_text(separator="\n", strip=True) if body else "Không có nội dung"

        results.append({
            "title": title,
            "date": date,
            "link": link,
            "description": lead_text,
            "content": content
        })

        print(f"✅ Crawled: {title}")

    except Exception as e:
        print(f"❌ Lỗi khi lấy bài {link}: {e}")

# 💾 Ghi dữ liệu ra file
with open("chungta.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n🎉 Đã lưu {len(results)} ")
