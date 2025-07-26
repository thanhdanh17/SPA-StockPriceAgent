import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

INPUT_FILE = "news_GAS.xlsx"
OUTPUT_FILE = "news_GAS_fix.xlsx"

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options)

def re_extract_from_link(driver, url):
    try:
        driver.get(url)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Crawl content
        content_div = soup.find("div", id="post_content")
        content = ""
        if content_div:
            paragraphs = content_div.find_all("p")
            content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        # Crawl AI summary
        try:
            ai_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Tóm tắt tin tức bằng AI')]"))
            )
            ai_button.click()
            time.sleep(10)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            ai_summary_tag = soup.select_one("div.italic:not(.font-bold)")
            ai_summary = ai_summary_tag.get_text(strip=True) if ai_summary_tag else ""
        except:
            ai_summary = ""

        return content, ai_summary

    except Exception as e:
        print(f"⚠️ Lỗi khi xử lý {url}: {e}")
        return "", ""

def repair_missing_data():
    df = pd.read_excel(INPUT_FILE)
    driver = setup_driver()

    for idx, row in df.iterrows():
        content_missing = pd.isna(row["content"]) or row["content"] == ""
        summary_missing = pd.isna(row["ai_summary"]) or row["ai_summary"] == ""

        if content_missing or summary_missing:
            print(f"🔄 Đang cập nhật dòng {idx+1}: {row['link']}")
            content, ai_summary = re_extract_from_link(driver, row["link"])

            if content_missing:
                df.at[idx, "content"] = content
            if summary_missing:
                df.at[idx, "ai_summary"] = ai_summary

    driver.quit()
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"✅ Hoàn tất cập nhật. Đã lưu vào: {OUTPUT_FILE}")

if __name__ == "__main__":
    repair_missing_data()
