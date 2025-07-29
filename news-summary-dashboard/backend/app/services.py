import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

def connect_postgres():
    conn = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    return conn

def get_news_from_db(industry=None):
    conn = connect_postgres()
    cursor = conn.cursor()
    base_query = """SELECT * FROM "fireant_data" 
                    WHERE "date" 
                    IN (SELECT DISTINCT "date" 
                        FROM "fireant_data" 
                        WHERE "date" IS NOT NULL
                        ORDER BY "date" 
                        DESC LIMIT 5
                        )"""
    
    params = []

    # Nếu có tham số industry được truyền vào, thêm điều kiện lọc
    if industry:
        base_query += ' AND "industry" = %s'
        params.append(industry)

    # Thêm dấu chấm phẩy để kết thúc câu lệnh
    base_query += ' ORDER BY "date" DESC;'
    
    # Thực thi câu lệnh với tham số một cách an toàn để chống SQL Injection
    cursor.execute(base_query, tuple(params))

    rows = cursor.fetchall()
    #print(rows)
    news_data = []
    for row in rows:
        data = {
            'date': row[11],
            'industry': row[7],
            'title': row[1],
            'summary': row[6],
            'influence_score': row[10], # lấy tạm của thằng summary_token_count
            'hashtags': row[8] # lấy tạm của thằng sentiment
        }
        data['date'] = str(data['date'])
        # 2025-06-30
        data['date'] = data['date'][8:10]+"/"+data['date'][5:7]+"/"+data['date'][0:4]

        # chuyển đổi tên ngành từ tiếng anh sang tiếng Việt
        if data['industry'] == "Finance":
            data['industry'] = "Tài chính"
        elif data['industry'] == "Technology":
            data['industry'] = "Công nghệ"
        elif data['industry'] == "Energy":
            data['industry'] = "Năng lượng"
        elif data['industry'] == "Healthcare":
            data['industry'] = "Sức khỏe"
        elif data['industry'] == "Other":
            data['industry'] = "Khác"

        # Chuyển đổi chuỗi hashtags thành một mảng (list).
        hashtags_string = data.get('hashtags') 
        if isinstance(hashtags_string, str):
            # Tách chuỗi thành list dựa vào khoảng trắng
            data['hashtags'] = hashtags_string.split() 
        else:
            # Nếu không phải string hoặc là None, trả về mảng rỗng
            data['hashtags'] = []

        # Tính toán màu sắc cho score
        try:
            score = int(data['influence_score'])
        except (ValueError, TypeError):
            score = 0  # Giá trị mặc định nếu không thể chuyển đổi thành số
            
        if score < 50:
            data['color'] = 'red.300'
        elif 50 <= score <= 75:
            data['color'] = 'yellow.300'
        else:
            data['color'] = 'green.300'
        
        news_data.append(data)
    cursor.close()
    conn.close()
    return news_data
