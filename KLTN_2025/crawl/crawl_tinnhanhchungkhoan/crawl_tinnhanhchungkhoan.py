# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import pandas as pd


# def crawl_detail_article_selenium(driver, article_url):
#     """Dùng Selenium để mở bài viết và lấy nội dung từ thẻ .article__body.cms-body"""
#     try:
#         driver.get(article_url)
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "article__body"))
#         )
#         soup = BeautifulSoup(driver.page_source, "html.parser")
#         content_div = soup.find("div", class_="article__body")
#         if content_div:
#             return content_div.get_text(separator="\n", strip=True)
#         else:
#             return None
#     except Exception as e:
#         print(f"⚠️ Lỗi khi lấy nội dung bằng Selenium: {e}")
#         return None



# def crawl_tag_page(url, max_articles=20, wait_time=10):
#     """Lấy danh sách bài từ trang tag và mở từng bài để lấy nội dung"""
#     options = Options()
#     # Bỏ comment dòng dưới nếu muốn chạy không hiện trình duyệt
#     # options.add_argument("--headless")
#     driver = webdriver.Chrome(options=options)

#     print(f"🚀 Đang mở: {url}")
#     driver.get(url)

#     # Chờ bài viết xuất hiện
#     try:
#         WebDriverWait(driver, wait_time).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "story"))
#         )
#     except:
#         print("❌ Không thấy bài viết nào.")
#         driver.quit()
#         return []

#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     article_elements = soup.find_all("article", class_="story")

#     print(f"📌 Số bài tìm được: {len(article_elements)}")

#     results = []
#     for art in article_elements[:max_articles]:
#         try:
#             title = art.find("h2", class_="story__heading").text.strip()
#             url = art.find("a")["href"]
#             date = art.find("div", class_="story__meta").text.strip() if art.find("div", class_="story__meta") else "N/A"

#             print(f"📖 {title}\n→ {url}")
#             body = crawl_detail_article_selenium(driver, url)
#             print(f"📝 Nội dung: {body[:150]}...\n" if body else "⚠️ Không có nội dung.\n")

#             results.append({
#                 "title": title,
#                 "url": url,
#                 "date": date,
#                 "body": body
#             })
#         except Exception as e:
#             print("⚠️ Lỗi khi xử lý bài:", e)

#     driver.quit()
#     return results


# def save_to_csv(articles, filename="duoc_articles.csv"):
#     df = pd.DataFrame(articles)
#     df.to_csv(filename, index=False)
#     print(f"✅ Đã lưu {len(df)} bài viết vào {filename}")




from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


def click_load_more(driver, max_clicks=30):
    """Tự động bấm nút 'XEM THÊM' nhiều lần để load thêm bài"""
    for i in range(max_clicks):
        try:
            btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "control__loadmore"))
            )
            driver.execute_script("arguments[0].click();", btn)
            print(f"🔁 Đã bấm XEM THÊM lần {i+1}")
            time.sleep(2)
        except:
            print("⛔ Không còn nút XEM THÊM hoặc bị ẩn.")
            break


def crawl_detail_article_selenium(driver, article_url):
    """Dùng Selenium để mở bài viết và lấy nội dung từ thẻ .article__body.cms-body"""
    try:
        driver.get(article_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "article__body"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        content_div = soup.find("div", class_="article__body")
        if content_div:
            return content_div.get_text(separator="\n", strip=True)
        else:
            return None
    except Exception as e:
        print(f"⚠️ Lỗi khi lấy nội dung bằng Selenium: {e}")
        return None


def crawl_page(driver, url, tag_name="unknown", max_articles=500, wait_time=10):
    print(f"\n🚀 Đang crawl: {url}")
    driver.get(url)

    # Bấm "XEM THÊM" nhiều lần nếu có
    click_load_more(driver, max_clicks=10)

    try:
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, "story"))
        )
    except:
        print("❌ Không thấy bài viết nào.")
        return []

    soup = BeautifulSoup(driver.page_source, "html.parser")
    article_elements = soup.find_all("article", class_="story")
    print(f"📌 Số bài trên trang sau load thêm: {len(article_elements)}")

    results = []
    for art in article_elements[:max_articles]:
        try:
            title = art.find("h2", class_="story__heading").text.strip()
            url = art.find("a")["href"]
            date = art.find("div", class_="story__meta").text.strip() if art.find("div", class_="story__meta") else "N/A"

            print(f"📖 {title}\n→ {url}")
            body = crawl_detail_article_selenium(driver, url)
            print(f"📝 Nội dung: {body[:150]}...\n" if body else "⚠️ Không có nội dung.\n")

            results.append({
                "title": title,
                "link": url,
                "published": date,
                "content": body
            })
        except Exception as e:
            print("⚠️ Lỗi khi xử lý bài:", e)

    return results


def crawl_multiple_pages(pages: dict, max_articles=500):
    """pages: dict { 'ten_tag': 'link' }"""
    options = Options()
    # options.add_argument("--headless")  # Bật nếu muốn chạy ngầm
    driver = webdriver.Chrome(options=options)

    all_results = []
    for tag, url in pages.items():
        articles = crawl_page(driver, url, tag_name=tag, max_articles=max_articles)
        all_results.extend(articles)

    driver.quit()
    return all_results


def save_to_csv(articles, filename="energy_01.csv"):
    df = pd.DataFrame(articles)
    df.to_csv(filename, index=False)
    print(f"✅ Đã lưu {len(df)} bài viết vào {filename}")
