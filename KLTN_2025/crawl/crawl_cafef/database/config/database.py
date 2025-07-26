from pymongo import MongoClient

# === CẤU HÌNH KẾT NỐI MONGODB ===
MONGO_URI = "mongodb+srv://spa_user:spa123456@cluster0.9psfv5i.mongodb.net/stock_price_agent?retryWrites=true&w=majority"
DB_NAME = "stock_price_agent"
COLLECTION_NAME = "raw_news"

def connect_mongo():
    """
    Kết nối tới MongoDB và trả về collection 'raw_news' trong database 'stock_price_agent'.
    """
    client = MongoClient(MONGO_URI)
    return client[DB_NAME][COLLECTION_NAME]
