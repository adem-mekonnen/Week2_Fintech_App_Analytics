```markdown
# Customer Experience Analytics for Ethiopian Fintech Apps

![Python](https://img.shields.io/badge/Python-3.10-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![Status](https://img.shields.io/badge/Status-Completed-green)

## 📌 Project Overview
This project involves scraping, analyzing, and visualizing Google Play Store reviews for three major Ethiopian banking applications:
1.  **Commercial Bank of Ethiopia (CBE)**
2.  **Bank of Abyssinia (BOA)**
3.  **Dashen Bank**

**Business Objective:**  
To identify key drivers of customer satisfaction and retention by extracting actionable insights (sentiments and themes) from unstructured user feedback using NLP and Data Engineering pipelines.

---

## 📂 Project Structure

```text
Fintech_App_Analytics/
│
├── .github/workflows/      # CI/CD Pipeline configuration
├── data/
│   ├── raw/                # Original scraped data
│   ├── processed/          # Cleaned & Analyzed CSVs
│   └── schema.sql          # Database Schema Dump (Task 3 KPI)
├── reports/
│   └── figures/            # Generated charts (PNGs)
├── scripts/                # Python modules
│   ├── config.py           # Configuration, Logging, & Paths
│   ├── scraper.py          # Task 1: Scrapes Google Play Store
│   ├── preprocessing.py    # Task 1: Cleans and normalizes data
│   ├── sentiment_analysis.py # Task 2: BERT Sentiment & Theme extraction
│   ├── db_loader.py        # Task 3: Loads data to PostgreSQL
│   ├── verify_db.py        # Task 3: Data Integrity Verification
│   ├── visualize.py        # Task 4: Generates Plots
│   └── generate_insights.py # Task 4: Automated Text Report
├── tests/                  # Unit tests
├── docker-compose.yml      # Database container configuration
└── requirements.txt        # Project dependencies
```

---

## ⚙️ Setup & Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YourUsername/Fintech_App_Analytics.git
    cd Fintech_App_Analytics
    ```

2.  **Environment Setup:**
    ```bash
    # Create Virtual Environment
    python -m venv venv
    source venv/bin/activate  # Windows: .\venv\Scripts\activate

    # Install Dependencies
    pip install -r requirements.txt
    ```

3.  **Database Config:**
    Ensure Docker is running. Create a `.env` file with your credentials (see `.env.example`).

---

## 🚀 Task 1: Data Collection & Preprocessing

**Objective:** Collect over 1,200 user reviews and prepare them for analysis.

### Methodology
*   **Source:** Google Play Store via `google-play-scraper`.
*   **Target Apps:** CBE, BOA, Dashen.
*   **Cleaning Steps:**
    1.  Removed exact duplicates based on User, Text, and Date.
    2.  Normalized dates to `YYYY-MM-DD`.
    3.  Renamed columns to standard schema (`review`, `rating`, `date`, `bank`, `source`).

**Execution:**
```bash
python scripts/scraper.py
python scripts/preprocessing.py
```

---

## 🧠 Task 2: Sentiment & Thematic Analysis

**Objective:** Quantify user sentiment and categorize feedback into actionable themes.

### Methodology
1.  **Sentiment Analysis:**
    *   **Model:** `distilbert-base-uncased-finetuned-sst-2-english` (Hugging Face).
    *   **Logic:** Classifies reviews as **POSITIVE** or **NEGATIVE** with a confidence score.
2.  **Thematic Analysis:**
    *   **Technique:** Keyword-based Rule Matching.
    *   **Themes Defined:** `Account Access`, `Transaction Performance`, `App Stability`, `UI/UX`, `Features`.

**Execution:**
```bash
python scripts/sentiment_analysis.py
```

---

## 🗄️ Task 3: PostgreSQL Database Storage

**Objective:** Design and implement a relational database to store processed data and verify integrity.

### Database Schema
The project uses a normalized schema hosted via Docker. The full schema definition is available in `data/schema.sql`.

**Table 1: `banks` (Lookup)**
| Column | Type | Description |
| :--- | :--- | :--- |
| `bank_id` | VARCHAR (PK) | App Package Name |
| `bank_name` | VARCHAR | Readable Name (e.g., Dashen Bank) |

**Table 2: `reviews` (Data)**
| Column | Type | Description |
| :--- | :--- | :--- |
| `review_id` | SERIAL (PK) | Unique ID |
| `bank_id` | VARCHAR (FK) | Links to `banks` |
| `review_text` | TEXT | Raw Review |
| `sentiment_label`| VARCHAR | POSITIVE/NEGATIVE |
| `identified_theme`| VARCHAR | Key Topic |

**Execution & Verification:**
```bash
# 1. Start Container
docker-compose up -d

# 2. Run Loader Script (Applies schema.sql)
python scripts/db_loader.py

# 3. Verify Data Integrity (KPI Check)
python scripts/verify_db.py
```

---

## 📊 Task 4: Visualization & Insights

**Objective:** Derive insights and visualize results for stakeholders.

### Key Deliverables
1.  **Visualizations (`scripts/visualize.py`):** Generates Sentiment Distribution, Pain Point Analysis, and Word Clouds.
2.  **Automated Insights (`scripts/generate_insights.py`):** Programmatically generates evidence-backed recommendations for each bank based on the analysis.

**Execution:**
```bash
# Generate Charts
python scripts/visualize.py

# Generate Text Report (Recommendations)
python scripts/generate_insights.py
```
*Visual outputs saved to: `reports/figures/`*

---

## 🧪 Testing & Quality
*   **CI/CD:** GitHub Actions pipeline executes linting and testing on push.
*   **Logging:** Centralized configuration via `scripts/config.py`.
*   **Local Test:**
    ```bash
    pytest
    ```

## 📝 Author
**Adem M**  
10 Academy AI  
Date: Dec 2025
```
