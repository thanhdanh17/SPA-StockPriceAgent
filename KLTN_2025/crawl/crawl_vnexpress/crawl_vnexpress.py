from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

# --- Khởi tạo trình duyệt ---
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Bỏ comment nếu không cần thấy browser
driver = webdriver.Chrome(options=options)

def crawl_article(driver, url):
    driver.get(url)
    time.sleep(2)

    try:
        title = driver.find_element(By.CSS_SELECTOR, "h1.title-detail").text
    except:
        title = ""

    try:
        date = driver.find_element(By.CSS_SELECTOR, "span.date").text
    except:
        date = ""

    try:
        paragraphs = driver.find_elements(By.CSS_SELECTOR, "article.fck_detail p.Normal")
        content = "\n".join([p.text for p in paragraphs if p.text.strip()])
    except:
        content = ""

    return {
        "title": title,
        "link": url,
        "date": date,
        "content": content
    }

# --- Crawl từng trang ---
all_articles = []
N = 5  # Số trang bạn muốn crawl

for page in range(1, N + 1):
    if page == 1:
        page_url = "https://vnexpress.net/khoa-hoc-cong-nghe/ai"
    else:
        page_url = f"https://vnexpress.net/khoa-hoc-cong-nghe/ai-p{page}"

    driver.get(page_url)
    time.sleep(3)
    print(f"\n--- Đang xử lý trang {page_url} ---")

    # Lấy danh sách link bài viết
    elements = driver.find_elements(By.CSS_SELECTOR, "article.item-news a[href]")
    raw_links = [el.get_attribute("href") for el in elements if el.get_attribute("href")]

    # Lọc bỏ trùng và bài video/quảng cáo
    links = list(set(link for link in raw_links if "/video/" not in link and "vnexpress.net" in link))

    print(f"Phát hiện {len(links)} bài viết")

    for i, link in enumerate(links):
        print(f"[{i+1}/{len(links)}] Crawling: {link}")
        try:
            article = crawl_article(driver, link)
            all_articles.append(article)
        except Exception as e:
            print(f"❌ Lỗi khi crawl {link}: {e}")

# Đóng trình duyệt
driver.quit()

# Lưu file JSON
with open("vnexpress_ai_articles.json", "w", encoding="utf-8") as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=2)

print(f"\n✅ Hoàn tất. Tổng số bài đã crawl: {len(all_articles)}")
