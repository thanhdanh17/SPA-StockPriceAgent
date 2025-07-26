from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
import os

def setup_driver():
    options = Options()
    # options.add_argument("--headless")  # Bỏ comment nếu không cần thấy browser
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    return driver

def extract_article_data(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")

    try:
        title_tag = soup.select_one("h1.title")
        date_tag = soup.select_one("span.pdate[data-role='publishdate']")
        content_container = soup.select_one("div.detail-content.afcbc-body")

        if not (title_tag and date_tag and content_container):
            print("⚠️ Không tìm thấy đầy đủ tiêu đề / ngày đăng / nội dung.")
            return None

        content_tags = content_container.select("p")
        content = " ".join(p.get_text(strip=True) for p in content_tags if p.get_text(strip=True))

        return {
            "title": title_tag.get_text(strip=True),
            "date": date_tag.get_text(strip=True),
            "content": content,
            "link": driver.current_url
        }
    except Exception as e:
        print(f"❌ Lỗi khi trích xuất dữ liệu bài viết: {e}")
        return None

def crawl_articles_sequentially(keyword="An Khang", max_pages=3):
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    all_articles = []

    for page in range(1, max_pages + 1):
        search_url = f"https://cafef.vn/tim-kiem/trang-{page}.chn?keywords={keyword.replace(' ', '%20')}"
        print(f"\n🔎 Trang {page}: {search_url}")
        driver.get(search_url)
        time.sleep(2)

        article_links = driver.find_elements(By.CSS_SELECTOR, "div.item h3.titlehidden a")
        print(f"  👉 Tìm thấy {len(article_links)} bài viết")

        for index in range(len(article_links)):
            try:
                article_links = driver.find_elements(By.CSS_SELECTOR, "div.item h3.titlehidden a")
                link_element = article_links[index]
                driver.execute_script("arguments[0].scrollIntoView();", link_element)
                time.sleep(1)

                driver.execute_script("arguments[0].click();", link_element)
                time.sleep(2)

                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.title")))
                except:
                    print(f"⚠️ Không load được bài viết {index+1}, bỏ qua.")
                    driver.get(search_url)
                    time.sleep(1)
                    continue

                data = extract_article_data(driver)
                if not data:
                    print(f"⚠️ Bài {index+1} không lấy được nội dung, bỏ qua.")
                    driver.get(search_url)
                    time.sleep(1)
                    continue

                all_articles.append(data)
                print(f"     ✅ Lấy bài: {data['title'][:60]}...")

                driver.get(search_url)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.item")))
                time.sleep(1)

            except Exception as e:
                print(f"❌ Lỗi tại bài {index + 1}: {e}")
                driver.get(search_url)
                time.sleep(3)

    driver.quit()

    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", "cafef_fpt.json"), "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"\n📦 Đã lưu {len(all_articles)} ")

# === CHẠY ===
if __name__ == "__main__":
    crawl_articles_sequentially(keyword="FPT", max_pages=160)
