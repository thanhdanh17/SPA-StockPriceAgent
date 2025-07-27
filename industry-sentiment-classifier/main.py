import torch
import logging
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import logging as transformers_logging
from utils.database import SupabaseConnector
from config import Config
import time
import os

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
transformers_logging.set_verbosity_error()  # Giảm mức độ logging từ transformers

class PhoBERTClassifier:
    def __init__(self, model_path, labels):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.labels = labels
        
        try:
            # Initialize tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
            
            # Load Model with classification head
            self.model = AutoModelForSequenceClassification.from_pretrained(
                "vinai/phobert-base",
                num_labels=len(labels),
                ignore_mismatched_sizes=True  # Bỏ qua cảnh báo kích thước không khớp
            )
            
            # Verify model file exists
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at: {model_path}")
            
            # Load weights
            model_weights = torch.load(model_path, map_location=self.device, weights_only=True)
            
            # Fix key names and filter classifier weights
            fixed_weights = {
                k.replace('bert.', '').replace('fc.', 'classifier.'): v 
                for k, v in model_weights.items()
                if not k.startswith('cls.')  # Bỏ qua các trọng số không cần thiết
            }
            
            # Load weights
            self.model.load_state_dict(fixed_weights, strict=False)
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"Model loaded successfully from {model_path}")
            
        except Exception as e:
            logger.error(f"Error initializing classifier: {str(e)}")
            raise

    def predict(self, text):
        try:
            inputs = self.tokenizer(
                text, 
                return_tensors="pt", 
                padding=True, 
                truncation=True, 
                max_length=256
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=1)
                pred_idx = torch.argmax(probs, dim=1).item()
            
            return self.labels[pred_idx], probs[0].cpu().numpy()
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return "Unknown", [0]*len(self.labels)

class ClassificationPipeline:
    def __init__(self):
        try:
            logger.info("Initializing classification pipeline...")
            
            # Verify model paths
            logger.info(f"Industry model path: {Config.MODEL_INDUSTRY_PATH}")
            logger.info(f"Sentiment model path: {Config.MODEL_SENTIMENT_PATH}")
            
            # Model initialization
            self.industry_classifier = PhoBERTClassifier(
                Config.MODEL_INDUSTRY_PATH,
                ['Finance', 'Technology', 'Healthcare', 'Energy', 'Other']
            )
            
            self.sentiment_classifier = PhoBERTClassifier(
                Config.MODEL_SENTIMENT_PATH,
                ['Positive', 'Negative', 'Neutral']
            )
            
            # Database connection
            self.db = SupabaseConnector()
            logger.info("All components initialized successfully")
            
        except Exception as e:
            logger.critical(f"Failed to initialize pipeline: {str(e)}")
            raise
    
    def process_batch(self, batch_size=10):
        """Process a batch of data from database"""
        try:
            rows = self.db.fetch_unprocessed_rows(limit=batch_size)
            
            if not rows:
                logger.info("No unprocessed rows found in database")
                return False
            
            processed_count = 0
            for row in rows:
                try:
                    summary = row.get(Config.SUMMARY_COLUMN, '')
                    if not summary:
                        continue
                    
                    # Perform classification
                    industry, _ = self.industry_classifier.predict(summary)
                    sentiment, _ = self.sentiment_classifier.predict(summary)
                    
                    # Update database
                    updates = {
                        Config.INDUSTRY_COLUMN: industry,
                        Config.SENTIMENT_COLUMN: sentiment
                    }
                    self.db.update_row(row['id'], updates)
                    processed_count += 1
                    
                    logger.info(f"Processed row {row['id']}: Industry={industry}, Sentiment={sentiment}")
                    
                except Exception as e:
                    logger.error(f"Error processing row {row.get('id', 'unknown')}: {str(e)}")
            
            logger.info(f"Successfully processed {processed_count}/{len(rows)} rows")
            return processed_count > 0
            
        except Exception as e:
            logger.error(f"Batch processing failed: {str(e)}")
            return False
    
    def run_continuous(self, batch_size=10, interval=60):
        """Run processing continuously with specified interval"""
        logger.info(f"Starting continuous processing (batch_size={batch_size}, interval={interval}s)")
        
        while True:
            try:
                if not self.process_batch(batch_size):
                    logger.info(f"Waiting {interval} seconds before next check...")
                    time.sleep(interval)
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt. Shutting down...")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                logger.info(f"Retrying in {interval} seconds...")
                time.sleep(interval)

if __name__ == "__main__":
    try:
        pipeline = ClassificationPipeline()
        pipeline.run_continuous(batch_size=10, interval=60)
    except Exception as e:
        logging.critical(f"Application failed: {str(e)}")
        raise