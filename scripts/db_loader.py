import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

# 2. Setup Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "reviews_analyzed.csv")

# 3. Database Connection Config
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Connection String
DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def setup_database():
    print(f"Connecting to database {DB_NAME} at {DB_HOST}:{DB_PORT}...")
    
    try:
        engine = create_engine(DATABASE_URI)
        
        # ---------------------------------------------------------
        # A. RESET SCHEMA (Drop old tables to fix 'Unknown' names)
        # ---------------------------------------------------------
        with engine.connect() as connection:
            print("⚠️ Dropping old tables to ensure fresh data...")
            connection.execute(text("DROP TABLE IF EXISTS reviews CASCADE;"))
            connection.execute(text("DROP TABLE IF EXISTS banks CASCADE;"))
            connection.commit()

        # ---------------------------------------------------------
        # B. DEFINE SCHEMA (Create Tables)
        # ---------------------------------------------------------
        create_banks_sql = """
        CREATE TABLE IF NOT EXISTS banks (
            bank_id VARCHAR(100) PRIMARY KEY,
            bank_name VARCHAR(100)
        );
        """
        
        create_reviews_sql = """
        CREATE TABLE IF NOT EXISTS reviews (
            review_id SERIAL PRIMARY KEY,
            bank_id VARCHAR(100) REFERENCES banks(bank_id),
            review_text TEXT,
            rating INT,
            review_date DATE,
            sentiment_label VARCHAR(50),
            sentiment_score FLOAT,
            identified_theme VARCHAR(100),
            source VARCHAR(50)
        );
        """

        with engine.connect() as connection:
            connection.execute(text(create_banks_sql))
            connection.execute(text(create_reviews_sql))
            connection.commit()
            print("✅ Tables 'banks' and 'reviews' created successfully.")

        # ---------------------------------------------------------
        # C. LOAD DATA
        # ---------------------------------------------------------
        if not os.path.exists(DATA_PATH):
            print(f"❌ Error: File not found at {DATA_PATH}")
            return

        df = pd.read_csv(DATA_PATH)
        print(f"📊 Loaded {len(df)} reviews from CSV.")

        # 1. Prepare 'banks' data
        unique_banks = df[['bank']].drop_duplicates().rename(columns={'bank': 'bank_id'})
        
        # --- FIX: Updated Map to match the Short Codes in your CSV ---
        name_map = {
            'CBE': 'Commercial Bank of Ethiopia',
            'BOA': 'Bank of Abyssinia',
            'Dashen': 'Dashen Bank'
        }
        unique_banks['bank_name'] = unique_banks['bank_id'].map(name_map).fillna('Unknown')

        # Insert Banks
        # We use 'append' because we just created empty tables above
        unique_banks.to_sql('banks', engine, if_exists='append', index=False)
        print("✅ Banks data inserted.")

        # 2. Prepare 'reviews' data
        reviews_to_db = df.rename(columns={
            'bank': 'bank_id',
            'review': 'review_text',
            'date': 'review_date'
        })
        
        # Select exact columns
        cols = ['bank_id', 'review_text', 'rating', 'review_date', 
                'sentiment_label', 'sentiment_score', 'identified_theme', 'source']
        
        if 'source' not in reviews_to_db.columns:
            reviews_to_db['source'] = 'Google Play'
            
        reviews_to_db = reviews_to_db[cols]

        # Insert Reviews
        reviews_to_db.to_sql('reviews', engine, if_exists='append', index=False)
        print("✅ Reviews data inserted successfully.")

        # ---------------------------------------------------------
        # D. VERIFICATION
        # ---------------------------------------------------------
        with engine.connect() as connection:
            # 1. Check Bank Names
            print("\n--- 🔍 Bank Names (Should be full names now) ---")
            result_banks = connection.execute(text("SELECT * FROM banks;"))
            for row in result_banks:
                print(row)
                
            # 2. Check Review Counts
            print("\n--- 🔍 Review Counts per Bank ---")
            result_counts = connection.execute(text("SELECT bank_id, COUNT(*) FROM reviews GROUP BY bank_id;"))
            for row in result_counts:
                print(f"   {row[0]}: {row[1]}")

    except Exception as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    setup_database()