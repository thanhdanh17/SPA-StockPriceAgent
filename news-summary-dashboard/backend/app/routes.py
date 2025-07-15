# backend/app/routes.py
from flask import Blueprint, jsonify
from .services import get_news_from_db

main = Blueprint('main', __name__)

@main.route('/api/news', methods=['GET'])
def get_news():
    data = get_news_from_db()  # Gọi hàm để lấy dữ liệu từ DB
    return jsonify(data)

@main.route('/')
def home():
    return "Hello, Flask!"