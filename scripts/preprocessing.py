import pandas as pd
import os

# Paths
RAW_FILE = os.path.join("data", "raw", "reviews_raw.csv")
PROCESSED_DIR = os.path.join("data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(PROCESSED_DIR, "reviews_cleaned.csv")

def preprocess_data():
    if not os.path.exists(RAW_FILE):
        print("Raw data file not found. Run scraper.py first.")
        return

    print("Loading raw data...")
    df = pd.read_csv(RAW_FILE)
    
    # Debug: Show columns found to ensure alignment
    print(f"Columns found: {df.columns.tolist()}")
    
    original_count = len(df)
    
    # 1. Handle Missing Data
    # ERROR FIX: Use 'review_text' and 'rating' (not content/score)
    df.dropna(subset=['review_text', 'rating'], inplace=True)
    
    # 2. Remove Duplicates
    # ERROR FIX: Use 'review_text' and 'review_date'
    df.drop_duplicates(subset=['review_text', 'bank_name', 'review_date'], inplace=True)
    
    # 3. Normalize Date
    # Ensure it is datetime objects, then strip to date
    df['date'] = pd.to_datetime(df['review_date']).dt.date
    
    # 4. Standardize Columns as per Requirements
    # Target columns: review, rating, date, bank, source
    df['source'] = 'Google Play' 
    
    # Rename to match final requirements
    df.rename(columns={
        'review_text': 'review',
        'bank_name': 'bank'
        # 'rating' is already named 'rating'
    }, inplace=True)
    
    # Select final columns
    final_df = df[['review', 'rating', 'date', 'bank', 'source']]
    
    # 5. Data Quality Check
    missing_percentage = final_df.isnull().mean().max() * 100
    
    print("\nPreprocessing Stats:")
    print(f"  - Original Records: {original_count}")
    print(f"  - Final Records:    {len(final_df)}")
    print(f"  - Duplicates/Nulls Removed: {original_count - len(final_df)}")
    print(f"  - Missing Data %:   {missing_percentage:.2f}%")
    
    # Save
    final_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nCleaned data saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    preprocess_data()