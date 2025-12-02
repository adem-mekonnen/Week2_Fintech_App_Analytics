import pandas as pd
from sqlalchemy import create_engine, text
# Import the Config class and the logger function
from config import Config, get_logger

# Initialize Logger
logger = get_logger("DB_LOADER")

def setup_database():
    logger.info("Starting Database Setup...")
    
    try:
        # 1. Connect using Config.DATABASE_URI
        engine = create_engine(Config.DATABASE_URI)
        
        # 2. Execute Schema from SQL File
        logger.info(f"Reading Schema from {Config.SCHEMA_PATH}")
        
        # Check if schema file exists
        if not Config.SCHEMA_PATH.exists():
            logger.error(f"Schema file not found at: {Config.SCHEMA_PATH}")
            return

        with open(Config.SCHEMA_PATH, 'r') as f:
            schema_sql = f.read()

        with engine.connect() as conn:
            # Drop and Recreate tables using the SQL file
            conn.execute(text(schema_sql))
            conn.commit()
            logger.info("✅ Schema Applied successfully.")

        # 3. Load Data with Validation
        if not Config.ANALYZED_DATA_PATH.exists():
            raise FileNotFoundError(f"{Config.ANALYZED_DATA_PATH} does not exist.")

        df = pd.read_csv(Config.ANALYZED_DATA_PATH)
        logger.info(f"📊 Loaded {len(df)} rows from CSV.")
        
        # 4. Prepare & Insert Banks
        banks = df[['bank']].drop_duplicates().rename(columns={'bank': 'bank_id'})
        name_map = {
            'CBE': 'Commercial Bank of Ethiopia', 
            'BOA': 'Bank of Abyssinia', 
            'Dashen': 'Dashen Bank'
        }
        banks['bank_name'] = banks['bank_id'].map(name_map).fillna('Unknown')
        
        # Insert Banks
        banks.to_sql('banks', engine, if_exists='append', index=False)
        logger.info(f"✅ Loaded {len(banks)} banks.")

        # 5. Prepare & Insert Reviews
        reviews = df.rename(columns={'bank': 'bank_id', 'review': 'review_text', 'date': 'review_date'})
        cols = ['bank_id', 'review_text', 'rating', 'review_date', 'sentiment_label', 'sentiment_score', 'identified_theme', 'source']
        
        # Ensure Source Column
        if 'source' not in reviews.columns: 
            reviews['source'] = 'Google Play'
        
        reviews[cols].to_sql('reviews', engine, if_exists='append', index=False)
        logger.info(f"✅ Loaded {len(reviews)} reviews.")

    except Exception as e:
        logger.error(f"❌ Database Operation Failed: {e}")

if __name__ == "__main__":
    setup_database()