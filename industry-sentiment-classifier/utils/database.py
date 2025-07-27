from supabase import create_client, Client
from config import Config
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

class SupabaseConnector:
    def __init__(self):
        try:
            # Validate config first
            if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
                raise ValueError("Supabase configuration is missing. Please check your .env file")
            
            self.client: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
            logging.info("Supabase client initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize Supabase client: {str(e)}")
            raise

    def fetch_unprocessed_rows(self, limit=100):
        """Get untreated rows (where Industry or Sentiment is NULL)"""
        try:
            response = self.client.table(Config.TABLE_NAME)\
                .select('*')\
                .or_(f"{Config.INDUSTRY_COLUMN}.is.null,{Config.SENTIMENT_COLUMN}.is.null")\
                .limit(limit)\
                .execute()
            
            logging.debug(f"Fetched {len(response.data)} unprocessed rows")
            return response.data
            
        except Exception as e:
            logging.error(f"Error fetching unprocessed rows: {str(e)}")
            return []

    def update_row(self, row_id, updates):
        """Update data for a specific row"""
        try:
            if not updates or not row_id:
                raise ValueError("Invalid update data or row ID")
            
            response = self.client.table(Config.TABLE_NAME)\
                .update(updates)\
                .eq('id', row_id)\
                .execute()
                
            logging.debug(f"Updated row {row_id} with {updates}")
            return response.data
            
        except Exception as e:
            logging.error(f"Error updating row {row_id}: {str(e)}")
            return None

    def health_check(self):
        """Check database connection"""
        try:
            self.client.table(Config.TABLE_NAME).select("id").limit(1).execute()
            return True
        except Exception:
            return False