import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

class Config:
    # --- Paths (Using Pathlib for better cross-OS support) ---
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "reviews_raw.csv"
    PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "reviews_cleaned.csv"
    ANALYZED_DATA_PATH = BASE_DIR / "data" / "processed" / "reviews_analyzed.csv"
    SCHEMA_PATH = BASE_DIR / "data" / "schema.sql"
    FIGURES_DIR = BASE_DIR / "reports" / "figures"

    # --- App IDs ---
    APPS = {
        'CBE': os.getenv('CBE_APP_ID', 'com.combanketh.mobilebanking'),
        'BOA': os.getenv('BOA_APP_ID', 'com.boa.boaMobileBanking'),
        'Dashen': os.getenv('DASHEN_APP_ID', 'com.dashen.dashensuperapp')
    }

    # --- Database Config ---
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'bank_reviews')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASS = os.getenv('DB_PASS', 'password')
    DB_PORT = os.getenv('DB_PORT', '5456')
    
    # Constructed URI for SQLAlchemy
    DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # --- Data Validation Schemas ---
    # Used to validate inputs in preprocessing and loading
    REQUIRED_COLUMNS_RAW = ['content', 'score', 'at', 'bank_package']
    REQUIRED_COLUMNS_ANALYZED = [
        'review', 'rating', 'date', 'bank', 
        'sentiment_label', 'sentiment_score', 'identified_theme'
    ]

# --- Structured Logging Setup ---
def get_logger(name):
    """
    Creates a standardized logger.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create console handler
        handler = logging.StreamHandler()
        
        # Create formatter (Time - Script Name - Level - Message)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    return logger