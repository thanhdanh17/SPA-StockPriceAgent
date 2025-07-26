from crawl_tinnhanhchungkhoan import crawl_multiple_pages, save_to_csv
from urllib.parse import quote

# Danh sách link tag + tìm kiếm
# pages_to_crawl = {
#     "nha-may-dien": "https://www.tinnhanhchungkhoan.vn/nha-may-dien-tag66447.html",
#     "than": "https://www.tinnhanhchungkhoan.vn/than-tag85968.html",
#     "gia-than": "https://www.tinnhanhchungkhoan.vn/gia-than-tag138836.html",
#     "dien-gio": "https://www.tinnhanhchungkhoan.vn/dien-gio-tag28877.html",
#     "nang-luong": "https://www.tinnhanhchungkhoan.vn/tim-kiem/?q=" + quote("năng lượng"),
#     "evn": "https://www.tinnhanhchungkhoan.vn/tim-kiem/?q=" + quote("EVN"),
#     "nhien-lieu": "https://www.tinnhanhchungkhoan.vn/tim-kiem/?q=" + quote("nhiên liệu"),
# }
pages_to_crawl = {
    # "yte": "https://www.tinnhanhchungkhoan.vn/tim-kiem/?q=y%20t%E1%BA%BF",
    "DHG": "https://www.tinnhanhchungkhoan.vn/tim-kiem/?q=DHG",
    "DMC": "https://www.tinnhanhchungkhoan.vn/tim-kiem/?q=CTCP%20Xu%E1%BA%A5t%20nh%E1%BA%ADp%20kh%E1%BA%A9u%20Y%20t%E1%BA%BF%20Domesco%09",
    "IMP" : "https://www.tinnhanhchungkhoan.vn/tim-kiem/?q=CTCP%20D%C6%B0%E1%BB%A3c%20ph%E1%BA%A9m%20Imexpharm%09",
    "JVC" : "https://www.tinnhanhchungkhoan.vn/tim-kiem/?q=CTCP%20Thi%E1%BA%BFt%20b%E1%BB%8B%20Y%20t%E1%BA%BF%20Vi%E1%BB%87t%20Nh%E1%BA%ADt",
}

# Crawl và lưu
articles = crawl_multiple_pages(pages_to_crawl, max_articles=100)
save_to_csv(articles, filename="crawl_heathcare_24.csv")
