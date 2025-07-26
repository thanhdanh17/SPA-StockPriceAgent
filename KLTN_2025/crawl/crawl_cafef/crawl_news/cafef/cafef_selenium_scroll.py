from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time
import sys
import os

# Kết nối MongoDB
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from database.config.database import connect_mongo

class CafeFCrawlerSeleniumScroll:
    def __init__(self, url: str, category: str, max_scroll=5):
        self.url = url
        self.category = category
        self.max_scroll = max_scroll
        self.collection = connect_mongo()

    def fetch_articles(self):
        options = Options()
        options.add_argument("--headless=new")  # hoặc "--headless"
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)
        print(f"📄 Đang mở: {driver.current_url}")

        for i in range(self.max_scroll):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            print(f"⬇ Scroll {i+1}")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        items = soup.select(".tlitem")
        print(f"✅ Tổng số bài viết tìm thấy: {len(items)}")
        articles = []

        for item in items:
            try:
                a_tag = item.select_one("a")
                link = "https://cafef.vn" + a_tag["href"]
                title = a_tag.get_text(strip=True)
                published = datetime.utcnow()

                # Truy cập chi tiết bài viết
                res = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
                article_soup = BeautifulSoup(res.text, "html.parser")

                selectors = [
                    ".detail-content.afcbc-body p",
                    ".bodytext p",
                    ".main-detail-body p"
                ]

                content = ""
                for sel in selectors:
                    paragraphs = article_soup.select(sel)
                    if paragraphs:
                        content = " ".join([p.get_text(strip=True) for p in paragraphs])
                        break

                doc = {
                    "title": title,
                    "link": link,
                    "published": published,
                    "content": content,
                    "source": "CafeF",
                    "category": self.category,
                    "created_at": datetime.utcnow()
                }

                self.collection.update_one({"link": link}, {"$set": doc}, upsert=True)
                articles.append(doc)

            except Exception as e:
                print(f"[!] Lỗi xử lý bài: {e}")
                continue

        return articles
