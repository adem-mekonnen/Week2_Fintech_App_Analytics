from sqlalchemy import create_engine, text
# Import Config class instead of individual variables
from config import Config, get_logger

# Initialize Logger
logger = get_logger("DB_VERIFY")

def verify_integrity():
    logger.info("🧪 Starting Data Integrity Check...")
    
    try:
        # Use Config.DATABASE_URI
        engine = create_engine(Config.DATABASE_URI)
        
        with engine.connect() as conn:
            # 1. Check Total Count
            result = conn.execute(text("SELECT COUNT(*) FROM reviews;"))
            total_count = result.scalar()
            logger.info(f"Total Rows Found: {total_count}")
            
            # KPI ASSERTION
            if total_count < 1000:
                logger.error("❌ KPI FAIL: Total reviews are less than 1,000.")
            else:
                logger.info("✅ KPI PASS: Total reviews > 1000.")

            # 2. Check Per-Bank Distribution
            logger.info("Checking Distribution per Bank:")
            result = conn.execute(text("SELECT bank_id, COUNT(*) FROM reviews GROUP BY bank_id;"))
            
            for row in result:
                bank_id, count = row
                if count >= 400:
                    logger.info(f"   ✅ {bank_id}: {count} reviews (Pass)")
                else:
                    logger.warning(f"   ⚠️ {bank_id}: {count} reviews (Low)")

            # 3. Check for Null Analysis
            result = conn.execute(text("SELECT COUNT(*) FROM reviews WHERE sentiment_label IS NULL;"))
            null_nlp = result.scalar()
            
            if null_nlp == 0:
                logger.info("✅ NLP Check: All reviews have Sentiment Analysis.")
            else:
                logger.error(f"❌ NLP Check: {null_nlp} reviews are missing NLP data.")

    except Exception as e:
        logger.error(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    verify_integrity()