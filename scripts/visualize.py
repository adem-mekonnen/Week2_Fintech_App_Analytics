import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# 1. Setup Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "reviews_analyzed.csv")
IMG_DIR = os.path.join(BASE_DIR, "reports", "figures")
os.makedirs(IMG_DIR, exist_ok=True)

def save_plot(filename):
    path = os.path.join(IMG_DIR, filename)
    plt.savefig(path, bbox_inches='tight', dpi=300)
    print(f"✅ Saved: {filename}")
    plt.close()

def create_visuals():
    if not os.path.exists(INPUT_FILE):
        print("❌ Error: Analyzed data not found. Run sentiment_analysis.py first.")
        return

    print("📊 Loading data...")
    df = pd.read_csv(INPUT_FILE)
    
    # Set global style
    sns.set_theme(style="whitegrid", palette="pastel")

    # --- PLOT 1: Overall Sentiment Distribution by Bank ---
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='bank', hue='sentiment_label', palette={'POSITIVE': '#2ecc71', 'NEGATIVE': '#e74c3c'})
    plt.title('Sentiment Distribution Comparison', fontsize=16)
    plt.xlabel('Bank Name')
    plt.ylabel('Count of Reviews')
    save_plot('1_sentiment_distribution.png')

    # --- PLOT 2: Average Ratings ---
    plt.figure(figsize=(8, 5))
    avg_rating = df.groupby('bank')['rating'].mean().reset_index().sort_values('rating', ascending=False)
    sns.barplot(data=avg_rating, x='bank', y='rating', palette='Blues_d')
    plt.ylim(0, 5)
    plt.title('Average User Rating (1-5 Stars)', fontsize=16)
    for index, row in avg_rating.iterrows():
        plt.text(index, row.rating + 0.1, round(row.rating, 2), color='black', ha="center")
    save_plot('2_avg_rating.png')

    # --- PLOT 3: Pain Points (Negative Themes) ---
    # Filter for negative reviews only
    neg_df = df[df['sentiment_label'] == 'NEGATIVE']
    if not neg_df.empty:
        plt.figure(figsize=(12, 6))
        # Count themes per bank
        sns.countplot(data=neg_df, x='identified_theme', hue='bank', palette='magma')
        plt.title('Key Pain Points (Themes in Negative Reviews)', fontsize=16)
        plt.xlabel('Identified Issue')
        plt.ylabel('Number of Complaints')
        plt.legend(title='Bank')
        save_plot('3_pain_points.png')

    # --- PLOT 4: Rating Distribution (Violin Plot) ---
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=df, x='bank', y='rating', palette='muted')
    plt.title('Rating Distribution Density', fontsize=16)
    save_plot('4_rating_density.png')

    # --- PLOT 5: Word Cloud for Negative Reviews ---
    text = " ".join(review for review in neg_df.review.astype(str))
    wordcloud = WordCloud(width=1600, height=800, background_color='white', colormap='Reds').generate(text)
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Most Common Words in Negative Reviews', fontsize=16)
    save_plot('5_negative_wordcloud.png')

if __name__ == "__main__":
    create_visuals()