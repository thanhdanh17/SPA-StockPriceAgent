from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from dateutil import parser
import time
import json

def parse_fuzzy_datetime(raw_text, current_year):
    raw_text = raw_text.lower().strip()
    try:
        if not raw_text:
            return None

        if "hôm nay" in raw_text:
            time_part = raw_text.replace("hôm nay", "").strip()
            dt = datetime.strptime(time_part, "%H:%M")
            today = datetime.now()
            return today.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0)

        if "hôm qua" in raw_text:
            time_part = raw_text.replace("hôm qua", "").strip()
            dt = datetime.strptime(time_part, "%H:%M")
            yesterday = datetime.now() - timedelta(days=1)
            return yesterday.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0)

        elif "khoảng" in raw_text or "trước" in raw_text:
            return None  # handled separately by ISO tag now

        else:
            dt = datetime.strptime(raw_text, "%d/%m %H:%M")
            return dt.replace(year=current_year)

    except Exception as e:
        print(f"⚠️ Lỗi parse fuzzy time: '{raw_text}' ({e})")
        return None

def format_datetime_obj(dt):
    return dt.strftime("%d-%m-%Y - %I:%M %p")

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options)

def scroll_and_collect_links(driver, stock_code="FPT", max_scrolls=20, scroll_step=600):
    url = f"https://fireant.vn/ma-chung-khoan/{stock_code}"
    driver.get(url)
    time.sleep(5)

    links = []
    scroll_position = 0

    for i in range(max_scrolls):
        print(f"🔽 Scroll {i+1}/{max_scrolls}")
        scroll_position += scroll_step
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(5)

        articles = driver.find_elements(By.CSS_SELECTOR, "div.flex.flex-row.h-full.border-b-1 a[href^='/bai-viet/']")
        for article in articles:
            try:
                href = article.get_attribute("href")
                if href and href.startswith("https://fireant.vn/bai-viet/"):
                    clean_href = href.split("?")[0]
                    if clean_href not in links:
                        links.append(clean_href)
            except:
                continue

        if scroll_position >= driver.execute_script("return document.body.scrollHeight"):
            break

    print(f"✅ Đã thu thập {len(links)} bài viết theo thứ tự từ trên xuống.")
    return links

def extract_article(driver, url):
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        title_tag = soup.select_one("div.mt-3.mb-5.text-3xl.font-semibold.leading-10")
        title = title_tag.get_text(strip=True) if title_tag else ""

        source, fuzzy_time = "", ""
        dt = None

        time_tag = soup.select_one("time[datetime]")
        if time_tag:
            fuzzy_time = time_tag.get_text(strip=True)
            try:
                raw_iso = time_tag.get("datetime") or time_tag.get("title")
                if raw_iso:
                    dt = parser.parse(raw_iso)
            except Exception as e:
                print(f"⚠️ Lỗi parse ISO datetime: {e}")

        if not dt:
            fuzzy_tags = soup.select("span.text-gray-500")
            if fuzzy_tags:
                for tag in fuzzy_tags:
                    parts = tag.get_text(strip=True).split("|")
                    if len(parts) == 2:
                        source = parts[0].strip()
                        fuzzy_time = parts[1].strip()
                    elif len(parts) == 1:
                        fuzzy_time = parts[0].strip()

        content_div = soup.find("div", id="post_content")
        content = ""
        if content_div:
            paragraphs = content_div.find_all("p")
            content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        try:
            ai_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Tóm tắt tin tức bằng AI')]"))
            )
            ai_button.click()
            time.sleep(8)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            ai_summary_tag = soup.select_one("div.italic:not(.font-bold)")
            ai_summary = ai_summary_tag.get_text(strip=True) if ai_summary_tag else ""
        except Exception as e:
            print(f"⚠️ AI summary lỗi: {e}")
            ai_summary = ""

        return {
            "title": title,
            "source": source,
            "link": url,
            "content": content,
            "ai_summary": ai_summary,
            "fuzzy_time": fuzzy_time,
        }
    except Exception as e:
        print(f"❌ Lỗi khi crawl bài viết: {url} ({e})")
        return {}

def crawl_articles_from_stock(stock_code="FPT"):
    driver = setup_driver()
    article_links = scroll_and_collect_links(driver, stock_code=stock_code, max_scrolls=10)

    current_year = 2025  # Đặt mốc cố định là năm hiện tại
    base_day_month = None
    results = []

    for idx, link in enumerate(article_links):
        print(f"📄 ({idx+1}/{len(article_links)}) {link}")
        raw_data = extract_article(driver, link)

        fuzzy_time = raw_data.get("fuzzy_time", "")
        dt = parse_fuzzy_datetime(fuzzy_time, current_year)

        if dt:
            current_day_month = (dt.month, dt.day)

            # Nếu là bài đầu tiên: đặt mốc chuẩn
            if base_day_month is None:
                base_day_month = current_day_month
            else:
                # Nếu bài mới có (month, day) > mốc gốc => đã sang năm cũ => trừ năm
                if current_day_month > base_day_month:
                    current_year -= 1
                    dt = dt.replace(year=current_year)
                    base_day_month = current_day_month  # cập nhật luôn mốc mới sau khi đổi năm

            raw_data["datetime"] = format_datetime_obj(dt)
        else:
            raw_data["datetime"] = ""

        results.append(raw_data)

    driver.quit()

    output_filename = f"data_{stock_code}_{datetime.now().strftime('%d%m%Y')}.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✅ Đã lưu {len(results)} bài viết vào {output_filename}")

if __name__ == "__main__":
    crawl_articles_from_stock("DBD")
