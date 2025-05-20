import feedparser
from datetime import datetime
import json
import sys
import os

# Add parent directory to sys.path to allow imports from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.config.database import connect_mongo

def load_rss_feeds(path="configs/rss_sources.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_rss_articles():
    rss_feeds = load_rss_feeds()
    collection = connect_mongo()

    for source, url in rss_feeds.items():
        print(f"Crawling source: {source}")
        feed = feedparser.parse(url)
        print(f"RSS {source} returned {len(feed.entries)} articles")

        if feed.entries:
            print("First article title:", feed.entries[0].title)

        new_count = 0
        for entry in feed.entries:
            if collection.find_one({"link": entry.link}):
                continue  # Skip if article already exists

            doc = {
                "title": entry.title,
                "link": entry.link,
                "published": entry.published if "published" in entry else None,
                "source": source,
                "scraped_at": datetime.utcnow(),
                "is_parsed": False
            }
            collection.insert_one(doc)
            new_count += 1

        print(f"Inserted {new_count} new articles from {source}.\n")

if __name__ == "__main__":
    fetch_rss_articles()
