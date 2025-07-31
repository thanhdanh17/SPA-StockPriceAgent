import time
from typing import List, Dict
from tqdm import tqdm
from database.supabase_handler import SupabaseHandler
from models.summarizer import NewsSummarizer
from config import Config
from utils.logger import logger
from utils.helpers import measure_performance

class SummarizationPipeline:
    """Enhanced pipeline for batch processing"""
    
    def __init__(self):
        self.db = SupabaseHandler()
        self.summarizer = NewsSummarizer()
        logger.info("Summarization pipeline initialized")
    
    @measure_performance
    def process_batch(self, batch_size: int = 20) -> int:
        """Process a batch of articles with improved logging"""
        total_success = 0
        while True:
            articles = self.db.fetch_unsummarized_articles(limit=batch_size)
            if not articles:
                if total_success == 0:
                    logger.info("No articles to process")
                break
            logger.info(f"Processing {len(articles)} articles")
            contents = [article["content"] for article in articles]
            try:
                summaries = self.summarizer.summarize_batch(contents)
                success_count = 0
                for article, summary in zip(articles, summaries):
                    if summary and self.db.update_summary(article["id"], summary):
                        success_count += 1
                logger.info(f"Successfully processed {success_count}/{len(articles)} articles")
                total_success += success_count
            except Exception as e:
                logger.error(f"Batch processing failed: {str(e)}")
                break
        return total_success

    def process_all_articles(self):
        """Process ALL unsummarized articles until completion"""
        total_processed = 0
        batch_size = Config.BATCH_SIZE
        
        with tqdm(desc="Processing ALL articles") as pbar:
            while True:
                articles = self.db.fetch_unsummarized_articles(limit=batch_size)
                if not articles:
                    break
                    
                contents = [article["content"] for article in articles]
                summaries = self.summarizer.summarize_batch(contents)
                
                batch_processed = 0
                for article, summary in zip(articles, summaries):
                    if summary and self.db.update_summary(article["id"], summary):
                        batch_processed += 1
                
                total_processed += batch_processed
                pbar.update(batch_processed)
                pbar.set_postfix({"Processed": total_processed})
                
                if Config.DEVICE == "cpu":
                    time.sleep(1)
        
        logger.info(f"FINISHED! Total articles processed: {total_processed}")
        return total_processed

if __name__ == "__main__":
    pipeline = SummarizationPipeline()
    pipeline.process_all_articles()