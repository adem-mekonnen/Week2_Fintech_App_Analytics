import pandas as pd
from transformers import pipeline
import os

# Paths
INPUT_FILE = os.path.join("data", "processed", "reviews_cleaned.csv")
OUTPUT_FILE = os.path.join("data", "processed", "reviews_analyzed.csv")

# Define Themes
THEMES = {
    "Account Access": ["login", "password", "otp", "sms", "code", "block"],
    "Transaction Issue": ["slow", "transfer", "failed", "pending", "network", "money"],
    "App Stability": ["crash", "close", "bug", "error", "open"],
    "UI/UX": ["design", "interface", "easy", "hard", "color", "look"],
    "Features": ["fingerprint", "telebirr", "update", "limit"]
}

def get_theme(text):
    text = str(text).lower()
    for theme, keywords in THEMES.items():
        if any(k in text for k in keywords):
            return theme
    return "General"

def run_analysis():
    if not os.path.exists(INPUT_FILE):
        print("Error: Cleaned data not found. Run preprocessing.py first for all banks .")
        return

    print("Loading Sentiment Model (this may take a moment)...")
    sentiment_pipe = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    
    print("Loading Data...")
    df = pd.read_csv(INPUT_FILE)
    
    print(f"Analyzing {len(df)} reviews...")
    
    # 1. Sentiment Analysis
    # Truncate text to 512 chars to prevent errors
    results = df['review'].astype(str).apply(lambda x: sentiment_pipe(x[:512])[0])
    
    df['sentiment_label'] = results.apply(lambda x: x['label'])
    df['sentiment_score'] = results.apply(lambda x: x['score'])
    
    # 2. Theme Extraction
    df['identified_theme'] = df['review'].apply(get_theme)
    
    # Save
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Success! Analyzed data with Sentiments & Themes saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_analysis()