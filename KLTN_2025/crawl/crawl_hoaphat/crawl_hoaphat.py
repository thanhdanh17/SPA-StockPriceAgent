from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

base_url = "https://www.hoaphat.com.vn/tin-tuc/tin-tuc-tap-doan?page="
articles = []

for page in range(1, 4):  # Crawl 3 trang đầu
    page_url = base_url + str(page)
    print(f"\n🌐 Đang xử lý: {page_url}")
    driver.get(page_url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = soup.select("ul.list-news li a")

    article_urls = []
    for a in links:
        href = a.get("href")
        if href and not href.startswith("http"):
            href = "https://www.hoaphat.com.vn" + href
        article_urls.append(href)

    print(f"  📌 Tìm được {len(article_urls)} bài trên trang {page}")

    for url in article_urls:
        try:
            driver.get(url)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ct-news-detail h1.title")))
            soup2 = BeautifulSoup(driver.page_source, "html.parser")

            title = soup2.select_one("div.ct-news-detail h1.title").get_text(strip=True)
            date = soup2.select_one("div.ct-news-detail div.date").get_text(strip=True)
            content = "\n".join(p.get_text(strip=True) for p in soup2.select("div.ct-news-detail div.content-news p"))

            articles.append({
                "url": url,
                "title": title,
                "date": date,
                "content": content
            })
            print("    ✅", title)

        except Exception as e:
            print("    ❌ Lỗi:", url, e)

driver.quit()

# Ghi ra Excel
df = pd.DataFrame(articles)
df.to_excel("hoaphat_news.xlsx", index=False)
print("\n✅ Đã lưu hoaphat_news.xlsx")
