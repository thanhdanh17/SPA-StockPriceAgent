import requests
from bs4 import BeautifulSoup
import sys
import os

# Add root path for cross-folder imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.config.database import connect_mongo

def extract_content_generic(url):
    """
    Fetch the full content of a news article from the provided URL.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Failed to access {url} - Status code: {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        # Remove unnecessary tags
        for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
            tag.decompose()

        # Extract paragraph text
        paragraphs = soup.find_all("p")
        text = "\n".join(
            p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 30
        )

        return text if text else None

    except Exception as e:
        print(f"❌ Error while fetching content from {url}: {e}")
        return None

def parse_unparsed_articles():
    """
    Find all unparsed articles in MongoDB and extract their full content.
    """
    collection = connect_mongo()
    unparsed_articles = list(collection.find({"is_parsed": False}))

    print(f"📝 Found {len(unparsed_articles)} unparsed articles")

    for article in unparsed_articles:
        print(f"🔗 Fetching content from: {article['link']}")
        content = extract_content_generic(article["link"])

        if content:
            collection.update_one(
                {"_id": article["_id"]},
                {"$set": {"content": content, "is_parsed": True}}
            )
            print("Content saved successfully")
        else:
            print("Failed to extract meaningful content")

if __name__ == "__main__":
    parse_unparsed_articles()
