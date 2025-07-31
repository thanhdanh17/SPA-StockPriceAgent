import os
import torch
from dotenv import load_dotenv
from typing import Dict, Any
from pathlib import Path

load_dotenv()

class Config:
    """Enhanced configuration with additional parameters"""
    
    # Hardware
    DEVICE = os.getenv("DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 5 if DEVICE == "cuda" else 2))
    
    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # Model paths
    MODEL_PATH = os.path.abspath(os.getenv("MODEL_PATH", "./vit5_summarization_finetuned"))
    
    # Text processing
    MAX_INPUT_LENGTH = int(os.getenv("MAX_INPUT_LENGTH", 1024))
    MAX_TARGET_LENGTH = int(os.getenv("MAX_TARGET_LENGTH", 256))
    
    # Performance
    MAX_ARTICLES_PER_RUN = int(os.getenv("MAX_ARTICLES_PER_RUN", 0))  # 0 = unlimited

    MAX_RETRIES = 3  # Try again when you encounter an error
    RETRY_DELAY = 5  # Waiting time between testing (seconds)
        
    @staticmethod
    def get_generation_config() -> Dict[str, Any]:
        config = {
            "max_length": Config.MAX_TARGET_LENGTH,
            "min_length": 30,
            "repetition_penalty": 1.2,
            "length_penalty": 1.0,
            "early_stopping": True,
            "no_repeat_ngram_size": 3 if Config.DEVICE == "cuda" else 2,
            "num_beams": 4 if Config.DEVICE == "cuda" else 2
        }
        return config