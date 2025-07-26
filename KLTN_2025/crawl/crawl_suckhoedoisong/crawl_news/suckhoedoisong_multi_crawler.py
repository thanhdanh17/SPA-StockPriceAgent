import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# === Setup selenium driver ===
options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(), options=options)
driver.set_page_load_timeout(15)

# === Load nguồn chuyên mục ===
with open("source_suckhoedoisong.json", "r", encoding="utf-8") as f:
    sources = json.load(f)

print(f"🔧 Tổng số chuyên mục cần crawl: {len(sources)}")

all_articles = []

# === Hàm chờ bài mới load thêm ===
def wait_new_articles(prev_count, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "a.box-category-link-title.cmtinited")) > prev_count
        )
        return True
    except TimeoutException:
        return False

for source in sources:
    url = source["url"]
    category = source["category"]

    print(f"\n🚀 Crawl bài viết từ chuyên mục {category} ({url})...")
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.box-category-link-title.cmtinited"))
        )
    except:
        print(f"❌ Không load được chuyên mục {category}")
        continue

    for _ in range(15):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        try:
            article_elems = driver.find_elements(By.CSS_SELECTOR, "a.box-category-link-title.cmtinited")
            prev_count = len(article_elems)

            view_more = driver.find_element(By.CSS_SELECTOR, "a.list__viewmore")
            if view_more.is_displayed():
                print("🔘 Bấm nút 'Hiển thị thêm bài'...")
                driver.execute_script("arguments[0].scrollIntoView(true);", view_more)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", view_more)

                loaded = wait_new_articles(prev_count)
                if not loaded:
                    print("⛔ Không thấy thêm bài mới.")
                    break
            else:
                break

        except Exception as e:
            print(f"⛔ Không thể click hoặc không còn nút: {e}")
            break

    soup = BeautifulSoup(driver.page_source, "html.parser")
    article_links = soup.select("a.box-category-link-title.cmtinited")
    links = ["https://suckhoedoisong.vn" + a["href"] for a in article_links if a.has_attr("href")]
    print(f"🔗 Số bài viết trong chuyên mục {category}: {len(links)}")

    for idx, link in enumerate(links, 1):
        print(f"📄 [{idx}/{len(links)}] Truy cập: {link}")
        try:
            driver.get(link)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.detail-title"))
            )
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.publish-date"))
            )

            soup = BeautifulSoup(driver.page_source, "html.parser")
            title_tag = soup.select_one("h1.detail-title")
            date_tag = soup.select_one("span.publish-date")
            paragraphs = soup.select("div.detail-content.afcbc-body p")

            if not title_tag or not date_tag:
                raise ValueError("Không tìm thấy title hoặc date")

            title = title_tag.get_text(strip=True)
            date = date_tag.get_text(strip=True)
            content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

            all_articles.append({
                "url": link,
                "title": title,
                "date": date,
                "content": content,
                "category": category
            })

        except Exception as e:
            print(f"❌ Lỗi ở bài {link}: {e}")
            continue

# === Lưu toàn bộ kết quả ===
output_path = "crawl_news/suckhoedoisong_articles.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=2)

print(f"\n✅ Hoàn tất! Đã lưu {len(all_articles)} bài vào {output_path}")
driver.quit()
