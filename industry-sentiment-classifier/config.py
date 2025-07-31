import os
from pathlib import Path
from dotenv import load_dotenv

# Load biến môi trường TRƯỚC KHI định nghĩa class
load_dotenv()

BASE_DIR = Path(__file__).parent

class Config:
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # In ra để debug
    print(f"Supabase URL: {SUPABASE_URL}")  
    print(f"Supabase KEY: {SUPABASE_KEY[:5]}...")  
    
    MODEL_INDUSTRY_PATH = BASE_DIR / 'models' / 'PhoBERT_industry_classificationv5.bin'
    MODEL_SENTIMENT_PATH = BASE_DIR / 'models' / 'PhoBERT_summary_sentiment.pth'

    TABLE_NAME = 'news'
    SUMMARY_COLUMN = 'summary'
    INDUSTRY_COLUMN = 'industry'
    SENTIMENT_COLUMN = 'sentiment'