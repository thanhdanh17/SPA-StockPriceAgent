import json
import time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    return webdriver.Chrome(options=options)

def extract_ai_summary(driver, url):
    try:
        driver.get(url)
        time.sleep(2)

        # Bấm nút tóm tắt
        ai_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Tóm tắt tin tức bằng AI')]"))
        )
        ai_button.click()

        # Đợi phần tóm tắt hiển thị
        ai_summary_tag = WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.italic:not(.font-bold)"))
        )
        return ai_summary_tag.text.strip()

    except Exception as e:
        print(f"⚠️ Không thể lấy AI summary từ {url}: {e}")
        return ""

def fill_missing_summaries(input_path="vip_VC.json", output_path="vip_VC_updated.json"):
    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    driver = setup_driver()
    updated = 0

    for idx, article in enumerate(articles):
        if not article.get("ai_summary"):
            print(f"📝 ({idx+1}/{len(articles)}) Đang xử lý lại: {article['link']}")
            summary = extract_ai_summary(driver, article["link"])
            if summary:
                article["ai_summary"] = summary
                updated += 1

    driver.quit()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã cập nhật {updated} bài viết có ai_summary bị thiếu.")

# 👉 Chạy chính
if __name__ == "__main__":
    fill_missing_summaries()
