import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # App IDs
    APPS = {
        'CBE': os.getenv('CBE_APP_ID', 'com.combanketh.mobilebanking'),
        'BOA': os.getenv('BOA_APP_ID', 'com.bankofabyssinia.mobileapp'),
        'Dashen': os.getenv('DASHEN_APP_ID', 'com.dashenbank.amele')
    }
    
    # Database Config
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'reviews_raw.csv')
    PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'reviews_cleaned.csv')
    ANALYZED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'reviews_analyzed.csv')