from flask import Flask, jsonify, request
from flask_cors import CORS
from .services import get_news_from_db # Dấu "." để import từ cùng thư mục "app"

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Kích hoạt CORS cho ứng dụng, cho phép mọi nguồn gốc truy cập
# Trong môi trường production, bạn nên giới hạn lại chỉ cho domain của frontend
CORS(app)

# Định nghĩa API endpoint tên là '/api/news'
@app.route('/api/news', methods=['GET'])
def news_endpoint():
    """
    Endpoint này sẽ được frontend gọi đến.
    Nó lấy dữ liệu từ database, chuyển thành JSON và trả về.
    """
    try:
        # Đọc tham số 'industry' từ URL query string
        industry_filter = request.args.get('industry')

        # Gọi hàm service và truyền giá trị filter vào
        news_data = get_news_from_db(industry=industry_filter)
        
        return jsonify(news_data)

    except Exception as e:
        print(f"Error fetching news: {e}")
        return jsonify({"error": "Không thể lấy dữ liệu từ server"}), 500