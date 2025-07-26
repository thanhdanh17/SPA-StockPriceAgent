import json
from crawl_news.cafef.cafef_selenium_scroll import CafeFCrawlerSeleniumScroll

def load_cafef_sources():
    with open("crawl_news/cafef/source_cafef.json", "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    sources = load_cafef_sources()

    for src in sources:
        url = src["url"]
        category = src["category"]
        print(f"\n🚀 Crawling: {category} - {url}")
        crawler = CafeFCrawlerSeleniumScroll(url, category, max_scroll=20)
        articles = crawler.fetch_articles()
        print(f"✅ Đã crawl {len(articles)} bài từ chuyên mục: {category}")
