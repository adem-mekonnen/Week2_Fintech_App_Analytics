### **Action:**
1.  Open the file named `README.md` in your root folder (`Fintech_App_Analytics/`).
2.  Delete any existing text.
3.  **Copy and paste** the markdown code below.

---

```markdown
# Customer Experience Analytics for Ethiopian Fintech Apps

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![Library](https://img.shields.io/badge/Library-HuggingFace%20Transformers-orange)

## 📌 Project Overview
This project involves scraping, analyzing, and visualizing Google Play Store reviews for three major Ethiopian banking applications:
1.  **Commercial Bank of Ethiopia (CBE)**
2.  **Bank of Abyssinia (BOA)**
3.  **Dashen Bank**

**Business Objective:**  
To identify key drivers of customer satisfaction and retention by extracting actionable insights (sentiments and themes) from unstructured user feedback.

---

## 📂 Project Structure

```text
Fintech_App_Analytics/
│
├── .github/workflows/      # CI/CD Pipeline configuration
├── data/
│   ├── raw/                # Original scraped data (reviews_raw.csv)
│   └── processed/          # Cleaned & Analyzed data (reviews_analyzed.csv)
├── notebooks/              # Jupyter Notebooks for visualization
├── reports/                # PDF deliverables
├── scripts/                # Python modules
│   ├── scraper.py          # Task 1: Scrapes Google Play Store
│   ├── preprocessing.py    # Task 1: Cleans and normalizes data
│   ├── sentiment_analysis.py # Task 2: BERT Sentiment & Theme extraction
│   └── db_loader.py        # Task 3: Loads data to PostgreSQL
└── tests/                  # Unit tests
```

---

## ⚙️ Setup & Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YourUsername/Fintech_App_Analytics.git
    cd Fintech_App_Analytics
    ```

2.  **Create Virtual Environment:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables:**
    Create a `.env` file in the root directory (see `.env.example` if available) to store database credentials.

---

## 🚀 Task 1: Data Collection & Preprocessing

**Objective:** Collect over 1,200 user reviews and prepare them for analysis.

### Methodology
*   **Source:** Google Play Store via `google-play-scraper`.
*   **Apps Targetted:**
    *   CBE: `com.combanketh.mobilebanking`
    *   BOA: `com.bankofabyssinia.mobileapp`
    *   Dashen: `com.dashenbank.amele`
*   **Cleaning Steps:**
    1.  Removed exact duplicates based on User, Text, and Date.
    2.  Normalized dates to `YYYY-MM-DD`.
    3.  Renamed columns to standard schema (`review`, `rating`, `date`, `bank`, `source`).

### Execution
To run the scraper and cleaner:
```bash
# 1. Scrape Data
python scripts/scraper.py

# 2. Clean Data
python scripts/preprocessing.py
```
*Output:* `data/processed/reviews_cleaned.csv`

---

## 🧠 Task 2: Sentiment & Thematic Analysis

**Objective:** Quantify user sentiment and categorize feedback into actionable themes.

### Methodology
1.  **Sentiment Analysis:**
    *   **Model:** `distilbert-base-uncased-finetuned-sst-2-english` (Hugging Face).
    *   **Logic:** Classifies reviews as **POSITIVE** or **NEGATIVE** with a confidence score.
2.  **Thematic Analysis:**
    *   **Technique:** Keyword-based Rule Matching.
    *   **Themes Defined:**
        *   `Account Access`: (login, otp, sms, password)
        *   `Transaction Performance`: (slow, lag, transfer, network)
        *   `App Stability`: (crash, close, error, bug)
        *   `UI/UX`: (design, interface, look, easy)
        *   `Customer Support`: (support, call, branch)

### Execution
To run the NLP pipeline:
```bash
python scripts/sentiment_analysis.py
```
*Output:* `data/processed/reviews_analyzed.csv` (Contains `sentiment_label`, `sentiment_score`, `identified_theme`).

---

## 🧪 Testing
This project uses GitHub Actions for CI/CD. To run tests locally:
```bash
pytest
```

## 📝 Author
**Adem M**  
1pacademy AI
Date: Dec 2025
```
