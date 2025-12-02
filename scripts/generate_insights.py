import pandas as pd
import sys
# Import Config class
from config import Config, get_logger

logger = get_logger("INSIGHTS")

def generate_recommendations():
    # Use Config.ANALYZED_DATA_PATH
    if not Config.ANALYZED_DATA_PATH.exists():
        logger.error(f"File not found: {Config.ANALYZED_DATA_PATH}")
        return

    df = pd.read_csv(Config.ANALYZED_DATA_PATH)
    logger.info("Generating Programmatic Insights...\n")

    # Map for clean names
    bank_map = {
        'CBE': 'Commercial Bank of Ethiopia',
        'BOA': 'Bank of Abyssinia',
        'Dashen': 'Dashen Bank'
    }

    print("="*60)
    print("AUTOMATED STRATEGIC INSIGHTS REPORT")
    print("="*60)

    for bank_code, bank_full in bank_map.items():
        bank_df = df[df['bank'] == bank_code]
        
        if bank_df.empty:
            continue

        # 1. Calculate Stats
        avg_rating = bank_df['rating'].mean()
        neg_reviews = bank_df[bank_df['sentiment_label'] == 'NEGATIVE']
        
        if not neg_reviews.empty:
            top_pain_point = neg_reviews['identified_theme'].mode()[0]
        else:
            top_pain_point = "None"
        
        print(f"\n🏦 {bank_full} ({bank_code})")
        print(f"   • Average Rating: {avg_rating:.2f}/5.0")
        print(f"   • Primary Pain Point: '{top_pain_point}'")

        # 2. Logic-Based Recommendations
        print("   👉 RECOMMENDATIONS (Evidence-Backed):")
        
        if top_pain_point == "App Stability":
            print("      1. CRITICAL: High volume of crash reports detected.")
            print("      2. ACTION: Halt feature rollouts and prioritize bug fixes.")
        elif top_pain_point == "Account Access":
            print("      1. HIGH: Users struggle to login (OTP/Password).")
            print("      2. ACTION: Implement Biometric Login to reduce OTP dependency.")
        elif top_pain_point == "Transaction Issue":
            print("      1. MEDIUM: Transaction speed is a friction point.")
            print("      2. ACTION: Add 'Skeleton Screens' to improve perceived performance.")
        else:
            print("      1. Monitor UI feedback for specific navigation issues.")

        # 3. Positive Driver
        pos_reviews = bank_df[bank_df['sentiment_label'] == 'POSITIVE']
        if not pos_reviews.empty:
            pos_theme = pos_reviews['identified_theme'].mode()[0]
            print(f"   ✅ Key Driver: Users respond well to '{pos_theme}'.")

if __name__ == "__main__":
    generate_recommendations()