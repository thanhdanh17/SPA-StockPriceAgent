import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from pathlib import Path
from config import Config
from utils.logger import logger
from typing import List
from tqdm import tqdm

class NewsSummarizer:
    """Optimized summarizer with batch processing"""
    
    def __init__(self):
        self.device = torch.device(Config.DEVICE)
        self._validate_model_path()
        self._load_model()
        self._warmup_model()
    
    def _validate_model_path(self):
        """Verify model files exist"""
        self.model_path = Path(Config.MODEL_PATH)
        required_files = ['config.json', 'model.safetensors', 
                         'tokenizer_config.json', 'spiece.model']
        
        missing = [f for f in required_files if not (self.model_path / f).exists()]
        if missing:
            raise FileNotFoundError(f"Missing model files: {missing}")

    def summarize_batch(self, texts: List[str]) -> List[str]:
        """Optimized batch processing with fallback"""
        if not texts:
            return []
            
        try:
            inputs = self.tokenizer(
                ["summarize: " + t for t in texts],
                max_length=Config.MAX_INPUT_LENGTH,
                truncation=True,
                padding="max_length",
                return_tensors="pt"
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    **Config.get_generation_config()
                )
            
            return [self.tokenizer.decode(o, skip_special_tokens=True).strip() 
                   for o in outputs]
            
        except Exception as e:
            logger.warning(f"Batch failed: {str(e)}")
            return [self.summarize(text) for text in texts]

    def _load_model(self):
        """Safely load tokenizer and model"""
        try:
            logger.info("Loading tokenizer...")
            self.tokenizer = T5Tokenizer.from_pretrained(
                str(self.model_path),
                legacy=False,
                local_files_only=True
            )
            
            logger.info("Loading model weights...")
            self.model = T5ForConditionalGeneration.from_pretrained(
                str(self.model_path),
                local_files_only=True
            ).to(self.device)
            
            self.model.eval()
            logger.info(f"Model loaded on {self.device}")
            
        except Exception as e:
            logger.error("Model loading failed")
            logger.error(f"Error details: {str(e)}")
            raise RuntimeError("Failed to initialize summarizer") from e

    def _warmup_model(self):
        """Initial inference to trigger lazy loading"""
        try:
            logger.info("Warming up model...")
            test_text = "This is a warmup run. " * 10
            self.summarize(test_text)
            logger.info("Model ready")
        except Exception as e:
            logger.warning(f"Warmup failed (non-critical): {str(e)}")

    def summarize(self, text: str) -> str:
        """Generate summary for single article with error handling"""
        if not text.strip():
            raise ValueError("Input text cannot be empty")
            
        try:
            input_text = "summarize: " + text.strip()
            
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt",
                max_length=Config.MAX_INPUT_LENGTH,
                truncation=True,
                padding="max_length"
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    **Config.get_generation_config()
                )
            
            return self._clean_output(outputs[0])
            
        except torch.cuda.OutOfMemoryError:
            logger.error("CUDA out of memory - reduce input length or batch size")
            raise
        except Exception as e:
            logger.error(f"Summarization failed for text: {text[:50]}...")
            logger.error(f"Error: {str(e)}")
            raise RuntimeError("Summarization failed") from e

    def summarize_batch(self, texts: List[str]) -> List[str]:
        """Batch processing with automatic fallback"""
        if not texts:
            return []
            
        # Automatic fallback to sequential on CPU or small batches
        if Config.DEVICE == "cpu" or len(texts) <= 2:
            return [self.summarize(text) for text in texts]
            
        try:
            input_texts = ["summarize: " + t.strip() for t in texts]
            
            inputs = self.tokenizer(
                input_texts,
                return_tensors="pt",
                max_length=Config.MAX_INPUT_LENGTH,
                truncation=True,
                padding="max_length"
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    **Config.get_generation_config()
                )
            
            return [self._clean_output(output) for output in outputs]
            
        except RuntimeError as e:
            logger.warning(f"Batch failed (falling back to sequential): {str(e)}")
            return [self.summarize(text) for text in texts]

    def _clean_output(self, output_tensor: torch.Tensor) -> str:
        """Clean and format model output"""
        return self.tokenizer.decode(
            output_tensor,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        ).strip()