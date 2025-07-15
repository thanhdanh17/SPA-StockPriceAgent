# backend/app/services.py
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

def get_news_from_db():
    conn = connect_postgres()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM "SPADashboardNews";""")
    rows = cursor.fetchall()
    #print(rows)
    news_data = []
    for row in rows:
        data = {
            'date': row[1],
            'industry': row[2],
            'title': row[3],
            'summary': row[4],
            'influence_score': row[5],
            'hashtags': row[6]
        }
        data['date'] = str(data['date'])
        # Tính toán màu sắc cho score
        try:
            score = int(data['influence_score'])
        except (ValueError, TypeError):
            score = 0  # Giá trị mặc định nếu không thể chuyển đổi thành số
            
        if score < 50:
            data['score'] = 'red.300'
        elif 50 <= score <= 75:
            data['score'] = 'yellow.300'
        else:
            data['score'] = 'green.300'
        
        news_data.append(data)
    cursor.close()
    conn.close()
    return news_data
