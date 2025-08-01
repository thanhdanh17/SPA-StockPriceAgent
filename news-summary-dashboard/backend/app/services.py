import redis
import json
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Khởi tạo Connection Pool một lần duy nhất khi module được tải
# Pool sẽ quản lý các kết nối đến Redis một cách hiệu quả.
try:
    # decode_responses=True nên được đặt ở đây để tất cả các kết nối từ pool đều có chung cài đặt này.
    pool = redis.ConnectionPool(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT"),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )

    # 2. Tạo một client Redis từ pool. 
    # Client này có thể được tái sử dụng trong toàn bộ ứng dụng.
    redis_client = redis.Redis(connection_pool=pool)

    # 3. Kiểm tra kết nối ban đầu để đảm bảo pool được cấu hình đúng
    redis_client.ping()
    print("Đã tạo Redis connection pool và client thành công.")

except redis.exceptions.ConnectionError as e:
    print(f"Lỗi kết nối Redis khi khởi tạo pool: {e}")
    redis_client = None # Đặt client là None nếu không thể kết nối
except Exception as e:
    print(f"Đã xảy ra lỗi không xác định khi khởi tạo Redis: {e}")
    redis_client = None

# Hàm get_redis_connection() ban đầu không còn cần thiết nữa.

def get_news_from_db(industry=None):
    """
    Hàm này lấy dữ liệu từ Redis sử dụng client đã kết nối qua connection pool.
    """
    # Kiểm tra xem client đã được khởi tạo thành công chưa
    if not redis_client:
        print("Redis client không khả dụng do lỗi kết nối ban đầu.")
        return []

    # Xác định đúng key trên Redis cần lấy
    if industry:
        # Nếu có filter, lấy key của ngành đó. Ví dụ: "news:Finance"
        redis_key = f"news:{industry}"
    else:
        # Nếu không có filter, lấy key chứa tất cả tin tức
        redis_key = "news:all"

    print(f"Đang lấy dữ liệu từ Redis với key: '{redis_key}'")

    try:
        # 4. Sử dụng client đã có sẵn, nó sẽ tự động quản lý kết nối từ pool.
        json_data = redis_client.get(redis_key)

        if not json_data:
            return [] # Trả về rỗng nếu không có dữ liệu

        # Dữ liệu trên Redis đã được xử lý sẵn, chỉ cần trả về
        return json.loads(json_data)

    except redis.exceptions.ConnectionError as e:
        # Lỗi này xảy ra nếu Redis bị ngắt kết nối trong quá trình hoạt động
        print(f"Mất kết nối tới Redis: {e}. Hãy thử lại sau.")
        return []
    except Exception as e:
        print(f"Đã xảy ra lỗi khi lấy dữ liệu từ Redis: {e}")
        return []