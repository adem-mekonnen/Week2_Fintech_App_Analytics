import pandas as pd
from transformers import pipeline
import os

INPUT_FILE = os.path.join("data", "processed", "reviews_cleaned.csv")
OUTPUT_FILE = os.path.join("data", "processed", "reviews_analyzed.csv")

# Keywords for themes
THEMES = {
    "Bugs/Crash": ["crash", "close", "bug", "error", "stuck"],
    "Performance": ["slow", "lag", "load", "wait", "network"],
    "UI/UX": ["design", "interface", "look", "easy", "hard"],
    "Features": ["transfer", "login", "otp", "fingerprint"]
}

def get_theme(text):
    text = str(text).lower()
    for theme, keywords in THEMES.items():
        if any(k in text for k in keywords):
            return theme
    return "General"

def analyze():
    print("Loading Model...")
    sentiment_pipe = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    
    df = pd.read_csv(INPUT_FILE)
    
    print("Analyzing Sentiment results for all banks ...")
    # Truncate to 512 tokens to avoid BERT errors
    df['sentiment_result'] = df['review'].apply(lambda x: sentiment_pipe(str(x)[:512])[0])
    df['sentiment_label'] = df['sentiment_result'].apply(lambda x: x['label'])
    df['sentiment_score'] = df['sentiment_result'].apply(lambda x: x['score'])
    df.drop(columns=['sentiment_result'], inplace=True)
    
    print("Extracting Themes...")
    df['theme'] = df['review'].apply(get_theme)
    
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Analysis Complete. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    analyze()