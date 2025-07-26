from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

options = Options()
# options.add_argument('--headless')  # Tắt nếu bạn muốn thấy trình duyệt
driver = webdriver.Chrome(options=options)

url = "https://simplize.vn/co-phieu/DBD/lich-su-gia"
driver.get(url)
wait = WebDriverWait(driver, 10)
time.sleep(5)

data = []
max_pages = 1 

for page in range(1, max_pages + 1):
    print(f"🔍 Crawling trang {page}...")
    time.sleep(2)

    # Lấy dữ liệu bảng
    rows = driver.find_elements(By.CSS_SELECTOR, 'tbody.simplize-table-tbody tr.simplize-table-row')
    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, 'td')
        if len(cells) >= 7:
            data.append({
                'Ngày': cells[0].text,
                'Giá mở cửa': cells[1].text,
                'Giá cao nhất': cells[2].text,
                'Giá thấp nhất': cells[3].text,
                'Giá đóng cửa': cells[4].text,
                'Thay đổi giá': cells[5].text,
                '% Thay đổi': cells[6].text,
                'Khối lượng': cells[7].text
            })

    # Click trang tiếp theo (nếu chưa phải cuối)
    if page < max_pages:
        try:
            # Tìm đúng <li> chứa số page (class luôn chứa thứ tự trang)
            selector = f"li.simplize-pagination-item-{page + 1} a"
            next_page = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", next_page)
        except Exception as e:
            print(f"❌ Lỗi khi click sang trang {page + 1}: {e}")
            break

driver.quit()

# Xuất ra Excel
df = pd.DataFrame(data)
df.to_excel("DBD.xlsx", index=False)
print("✅ Hoàn tất!")
