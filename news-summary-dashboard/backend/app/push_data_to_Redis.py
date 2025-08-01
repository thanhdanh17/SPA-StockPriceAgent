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

def sync_postgres_to_redis():
    logging.info("Bắt đầu quá trình đồng bộ...")
    pg_conn = None
    try:
        # 1. LẤY TOÀN BỘ DỮ LIỆU CỦA 5 NGÀY GẦN NHẤT
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

        # 2. XỬ LÝ VÀ PHÂN LOẠI DỮ LIỆU THEO NGÀNH
        
        # Tạo một dictionary để chứa dữ liệu đã được phân loại
        data_by_industry = {
            "Finance": [],
            "Technology": [],
            "Energy": [],
            "Healthcare": [],
            "Other": [],
            "all": [] # Thêm một mục để chứa tất cả dữ liệu
        }

        for row in rows:
            # --- Logic xử lý cho mỗi dòng (giữ nguyên) ---
            formatted_date = row['date'].strftime('%d/%m/%Y') if row.get('date') else ""
            
            data = {
                'date': formatted_date,
                'industry': row.get('industry', ''),
                'title': row.get('title', ''),
                'summary': row.get('summary', ''),
                'influence_score': row.get('summary_token_count', 0),
                'hashtags': row.get('sentiment', '')
            }

            original_industry = data['industry'] # Lưu lại tên ngành gốc (tiếng Anh)

            industry_map = {"Finance": "Tài chính", "Technology": "Công nghệ", "Energy": "Năng lượng", "Healthcare": "Sức khỏe", "Other": "Khác"}
            data['industry'] = industry_map.get(data['industry'], data['industry'])
            
            hashtags_map = {"Positive": "Tích_cực", "Negative": "Tiêu_cực", "Neutral": "Trung_tính"}
            data['hashtags'] = hashtags_map.get(data['hashtags'], data['hashtags'])
            data['hashtags'] = data['hashtags'].split() if isinstance(data['hashtags'], str) else []

            try:
                score = int(data['influence_score'])
            except (ValueError, TypeError):
                score = 0
            if score < 50: data['color'] = 'red.300'
            elif 50 <= score <= 75: data['color'] = 'yellow.300'
            else: data['color'] = 'green.300'
            # --- Kết thúc logic xử lý ---

            # Thêm dữ liệu đã xử lý vào đúng danh sách ngành (dựa trên tên gốc)
            if original_industry in data_by_industry:
                data_by_industry[original_industry].append(data)
            
            # Luôn thêm vào danh sách 'all'
            data_by_industry["all"].append(data)

        logging.info("Xử lý và phân loại dữ liệu hoàn tất.")

        # 3. ĐẨY DỮ LIỆU ĐÃ PHÂN LOẠI LÊN REDIS
        redis_conn = get_redis_connection()
        
        # Sử dụng pipeline để gửi nhiều lệnh cùng lúc, hiệu quả hơn
        with redis_conn.pipeline() as pipe:
            # Lặp qua từng ngành trong dictionary đã tạo
            for industry_name, data_list in data_by_industry.items():
                if data_list: # Chỉ đẩy lên nếu có dữ liệu
                    # Tạo key động, ví dụ: "news:Finance", "news:all"
                    redis_key = f"news:{industry_name}"
                    json_data = json.dumps(data_list, ensure_ascii=False)
                    # Đặt thời gian hết hạn là 1 ngày
                    pipe.set(redis_key, json_data, ex=86400)
                    logging.info(f"Đã chuẩn bị đẩy {len(data_list)} mục cho key '{redis_key}'.")
            
            # Thực thi tất cả các lệnh đã chuẩn bị
            pipe.execute()
        
        logging.info("Đã đẩy thành công tất cả các key lên Redis.")
        return len(rows)

    except Exception as e:
        logging.error(f"Đã xảy ra lỗi trong quá trình đồng bộ: {e}")
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