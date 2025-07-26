from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import json

# === Format thời gian ISO hoặc dạng ngắn như "28/6 10:33"
def format_datetime_obj(dt):
    return dt.strftime("%d-%m-%Y - %I:%M %p")

def parse_fuzzy_datetime(text):
    try:
        dt = datetime.strptime(text.strip(), "%d/%m %H:%M")
        dt = dt.replace(year=datetime.now().year)
        return dt
    except Exception as e:
        print(f"⚠️ Không phân tích được thời gian fuzzy: '{text}' ({e})")
        return datetime.now()

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    return webdriver.Chrome(options=options)

def scroll_and_collect_links(driver, max_scrolls=25):
    driver.get("https://fireant.vn/bai-viet")
    time.sleep(3)
    links = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(max_scrolls):
        print(f"🔽 Scroll {i+1}/{max_scrolls}")
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(4)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        article_tags = soup.select("a[href^='/bai-viet/']")

        for tag in article_tags:
            href = tag.get("href")
            if href and href.startswith("/bai-viet/"):
                full_url = "https://fireant.vn" + href.split("?")[0]
                links.add(full_url)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print(f"✅ Đã thu thập {len(links)} bài viết.")
    return list(links)

def get_ai_summary(driver):
    summary = ""
    try:
        ai_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Tóm tắt tin tức bằng AI')]"))
        )
        ai_button.click()
        print("🟢 Click lần 1: đã bấm nút tóm tắt")

        ai_summary_tag = WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.italic:not(.font-bold)"))
        )
        summary = ai_summary_tag.text.strip()
        print("✅ Lấy được tóm tắt lần 1")

    except Exception as e1:
        print("⚠️ Lần 1 không ra tóm tắt, thử lại lần 2...")
        try:
            time.sleep(3)
            ai_button_retry = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Tóm tắt tin tức bằng AI')]"))
            )
            ai_button_retry.click()
            print("🔁 Click lần 2: đã bấm lại nút")

            ai_summary_tag_retry = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.italic:not(.font-bold)"))
            )
            summary = ai_summary_tag_retry.text.strip()
            print("✅ Lấy được tóm tắt lần 2")

        except Exception as e2:
            print(f"❌ Retry lần 2 thất bại: {e2}")
            summary = ""

    return summary

def extract_article(driver, url):
    try:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        title_tag = soup.select_one("div.mt-3.mb-5.text-3xl.font-semibold.leading-10")
        title = title_tag.get_text(strip=True) if title_tag else ""

        fuzzy_tags = soup.select("span.text-gray-500")
        source, fuzzy_time = "", ""
        if fuzzy_tags:
            for tag in fuzzy_tags:
                parts = tag.get_text(strip=True).split("|")
                if len(parts) == 2:
                    source = parts[0].strip()
                    fuzzy_time = parts[1].strip()
                elif len(parts) == 1:
                    fuzzy_time = parts[0].strip()

        time_tag = soup.find("time")
        if time_tag and time_tag.has_attr("datetime"):
            try:
                dt = datetime.fromisoformat(time_tag["datetime"].replace("Z", "+00:00"))
            except:
                dt = parse_fuzzy_datetime(fuzzy_time)
        else:
            dt = parse_fuzzy_datetime(fuzzy_time)

        formatted_time = format_datetime_obj(dt)

        content_div = soup.find("div", id="post_content")
        content = ""
        if content_div:
            paragraphs = content_div.find_all("p")
            content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        ai_summary = get_ai_summary(driver)

        return {
            "title": title,
            "datetime": formatted_time,
            "source": source,
            "link": url,
            "content": content,
            "ai_summary": ai_summary
        }
    except Exception as e:
        print(f"❌ Lỗi khi crawl bài viết: {url} ({e})")
        return {}

def crawl_articles_from_homepage():
    driver = setup_driver()
    article_links = scroll_and_collect_links(driver, max_scrolls=5)

    results = []
    for idx, link in enumerate(article_links, 1):
        print(f"📄 ({idx}/{len(article_links)}) Đang xử lý: {link}")
        result = extract_article(driver, link)
        if result:
            results.append(result)

    driver.quit()

    with open("fireant_full_articles_29.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã lưu tất cả {len(results)} bài viết vào fireant_full_articles.json")
    print(f"🧠 Có {sum(1 for x in results if x['ai_summary'])} bài có ai_summary.")
    print(f"😶 Có {sum(1 for x in results if not x['ai_summary'])} bài bị thiếu.")

if __name__ == "__main__":
    crawl_articles_from_homepage()
