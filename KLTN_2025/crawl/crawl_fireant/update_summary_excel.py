import pandas as pd
import time
from bs4 import BeautifulSoup
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

        ai_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Tóm tắt tin tức bằng AI')]"))
        )
        ai_button.click()

        ai_summary_tag = WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.italic:not(.font-bold)"))
        )
        return ai_summary_tag.text.strip()

    except Exception as e:
        print(f"⚠️ Không thể lấy AI summary từ {url}: {e}")
        return ""

def fill_ai_summary_excel(input_excel="vip_vc.xlsx", output_excel="vipvc_filled.xlsx"):
    df = pd.read_excel(input_excel)

    if 'link' not in df.columns or 'ai_summary' not in df.columns:
        raise ValueError("Excel phải có cột 'link' và 'ai_summary'.")

    driver = setup_driver()
    updated_count = 0

    for i, row in df.iterrows():
        if pd.isna(row['ai_summary']) or row['ai_summary'].strip() == "":
            url = row['link']
            print(f"📝 Đang xử lý lại: {url}")
            summary = extract_ai_summary(driver, url)
            df.at[i, 'ai_summary'] = summary
            updated_count += 1

    driver.quit()
    df.to_excel(output_excel, index=False)
    print(f"✅ Đã cập nhật {updated_count} bài viết bị thiếu và lưu vào: {output_excel}")

# 👉 Gọi hàm chính
if __name__ == "__main__":
    fill_ai_summary_excel()
