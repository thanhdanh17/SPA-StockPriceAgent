import psycopg2
import psycopg2.extras
import redis
import json
from dotenv import load_dotenv
import os
import logging # Thư viện logging chuyên nghiệp
from fastapi import FastAPI, HTTPException

# --- CẤU HÌNH LOGGING ---
# Sử dụng logging thay cho print để dễ quản lý hơn trên server
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# --- CẤU HÌNH VÀ KẾT NỐI ---
def get_db_connection():
    load_dotenv()
    conn = psycopg2.connect(user=os.getenv("user"), password=os.getenv("password"), host=os.getenv("host"), port=os.getenv("port"), dbname=os.getenv("dbname"))
    return conn

def get_redis_connection():
    load_dotenv()
    r = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), password=os.getenv("REDIS_PASSWORD"), decode_responses=True)
    return r

# --- HÀM LOGIC ĐỒNG BỘ ---
def sync_postgres_to_redis():
    logging.info("Bắt đầu quá trình đồng bộ...")
    pg_conn = None
    try:
        # 1. LẤY DỮ LIỆU TỪ POSTGRES
        pg_conn = get_db_connection()
        cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = """
            SELECT * FROM "fireant_data" WHERE "date" IN (
                SELECT DISTINCT "date" FROM "fireant_data" WHERE "date" IS NOT NULL ORDER BY "date" DESC LIMIT 5
            ) ORDER BY "date" DESC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        logging.info(f"Đã lấy được {len(rows)} dòng dữ liệu từ PostgreSQL.")

        # 2. XỬ LÝ DỮ LIỆU (Giữ nguyên logic của bạn)
        processed_data = []
        for row in rows:
            formatted_date = ""
            if row.get('date'):
                formatted_date = row['date'].strftime('%d/%m/%Y')
            
            data = {
                'date': formatted_date,
                'industry': row.get('industry', ''),
                'title': row.get('title', ''),
                'summary': row.get('summary', ''),
                'influence_score': row.get('summary_token_count', 0),
                'hashtags': row.get('sentiment', '')
            }
            # Chuyển ngữ tên ngành
            industry_map = {
                "Finance": "Tài chính", "Technology": "Công nghệ",
                "Energy": "Năng lượng", "Healthcare": "Sức khỏe", "Other": "Khác"
            }
            data['industry'] = industry_map.get(data['industry'], data['industry'])
            
            # Xử lý hashtags
            hashtags_string = data.get('hashtags', '')
            data['hashtags'] = hashtags_string.split() if isinstance(hashtags_string, str) else []

            # Tính toán màu sắc
            try:
                score = int(data['influence_score'])
            except (ValueError, TypeError):
                score = 0
            if score < 50: data['color'] = 'red.300'
            elif 50 <= score <= 75: data['color'] = 'yellow.300'
            else: data['color'] = 'green.300'
            
            processed_data.append(data)
        
        logging.info("Xử lý dữ liệu hoàn tất.")

        # 3. ĐẨY DỮ LIỆU LÊN REDIS
        if processed_data:
            redis_conn = get_redis_connection()
            redis_key = "news:latest_5_days"
            json_data = json.dumps(processed_data, ensure_ascii=False)
            redis_conn.set(redis_key, json_data, ex=86400)
            logging.info(f"Đã đẩy thành công {len(processed_data)} mục vào Redis với key '{redis_key}'.")
        
        return len(processed_data) # Trả về số lượng bản ghi đã đồng bộ

    except Exception as e:
        logging.error(f"Đã xảy ra lỗi trong quá trình đồng bộ: {e}")
        # Ném lỗi ra ngoài để endpoint có thể bắt được
        raise e
    finally:
        if pg_conn:
            pg_conn.close()
            logging.info("Đã đóng kết nối PostgreSQL.")


# --- TẠO ỨNG DỤNG VÀ API ENDPOINT ---

app = FastAPI()

# --- ENDPOINT MỚI ĐƯỢC THÊM VÀO ---
@app.get("/")
async def health_check():
    """
    Endpoint này chỉ dùng để kiểm tra xem server có hoạt động không.
    Google Apps Script sẽ gọi đến đây để giữ cho server không bị "ngủ".
    """
    return {"status": "alive"}


@app.post("/push_data")
async def trigger_sync_endpoint():
    """
    Endpoint này được gọi bởi n8n để kích hoạt quá trình đồng bộ dữ liệu.
    """
    try:
        # Gọi hàm logic chính
        record_count = sync_postgres_to_redis()
        # Trả về thông báo thành công
        return {"status": "success", "message": f"Data synced successfully. {record_count} records processed."}
    except Exception as e:
        # Nếu có lỗi, trả về mã lỗi 500
        raise HTTPException(status_code=500, detail=str(e))