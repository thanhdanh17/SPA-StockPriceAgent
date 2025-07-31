import supabase
from typing import List, Dict
from config import Config
from utils.logger import logger

class SupabaseHandler:
    """Handles all Supabase database operations with improved querying"""
    
    def __init__(self):
        self.client = supabase.create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        logger.info("Supabase client initialized")
    
    def fetch_unsummarized_articles(self, limit: int = 100) -> List[Dict]:
        """Fetch articles with improved query"""
        try:
            query = self.client.table("news")\
                .select("id, content")\
                .or_("summary.is.null,summary.eq.''")\
                .neq("content", "")\
                .order("created_at", desc=True)\
                .limit(limit)
            
            result = query.execute()
            return [a for a in result.data if a.get("content")]
        except Exception as e:
            logger.error(f"Fetch error: {e}")
            return []
    
    def update_summary(self, article_id: str, summary: str) -> bool:
        """Update article with generated summary"""
        try:
            response = self.client.table("news")\
                .update({"summary": summary})\
                .eq("id", article_id)\
                .execute()
            return True
        except Exception as e:
            logger.error(f"Error updating article {article_id}: {e}")
            return False