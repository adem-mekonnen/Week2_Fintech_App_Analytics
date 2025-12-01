from google_play_scraper import Sort, reviews
import pandas as pd
import os

# 1. CORRECT APP IDS
APP_PACKAGES = [
    'com.combanketh.mobilebanking',  # <-- FIXED: The correct ID for CBE
    'com.boa.boaMobileBanking',      # Working (as per your output)
    'com.dashen.dashensuperapp'      # Working (as per your output)
]

# 2. Setup Output Directory
RAW_DATA_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

all_reviews = []

print("Starting Scraping Process...")

for app_id in APP_PACKAGES:
    print(f"Scraping {app_id}...")
    
    try:
        result, _ = reviews(
            app_id,
            lang='en', 
            country='et', # 'et' is good for local apps, 'us' often works too
            sort=Sort.NEWEST, 
            count=600 
        )
        
        # Add the bank ID to the data
        for r in result:
            r['bank_package'] = app_id
            all_reviews.append(r)
            
        print(f" -> Successfully fetched {len(result)} reviews.")
        
    except Exception as e:
        print(f" -> Error scraping {app_id}: {e}")

# 3. Create DataFrame and Preprocess
if all_reviews:
    df = pd.DataFrame(all_reviews)
    
    # Select specific columns
    df = df[['content', 'score', 'at', 'bank_package']]
    df.columns = ['review_text', 'rating', 'review_date', 'bank_id']

    # Preprocessing: Date normalization & Drop duplicates
    df['review_date'] = pd.to_datetime(df['review_date']).dt.date
    df.drop_duplicates(inplace=True)

    # Map the package names to readable Bank Names
    name_map = {
        'com.combanketh.mobilebanking': 'CBE',
        'com.boa.boaMobileBanking': 'BOA',
        'com.dashen.dashensuperapp': 'Dashen'
    }
    # Use .map but fill NaN with the ID itself if mapping fails (safety check)
    df['bank_name'] = df['bank_id'].map(name_map).fillna(df['bank_id'])

    # Save to the correct folder structure
    output_path = os.path.join(RAW_DATA_DIR, "reviews_raw.csv")
    df.to_csv(output_path, index=False)
    
    print(f"\nScraping Complete. Data saved to: {output_path}")
    print(f"Total reviews collected: {len(df)}")
else:
    print("\nNo reviews were collected. Check your internet connection to check.")