Here is the completely updated **`README.md`** file.

It now includes **Task 3 (Database Schema)** and **Task 4 (Visualization)**, reflecting the full scope of your project.
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
├── notebooks/              # Jupyter Notebooks for interactive analysis
├── reports/
│   └── figures/            # Generated charts (PNGs)
├── scripts/                # Python modules
│   ├── scraper.py          # Task 1: Scrapes Google Play Store
│   ├── preprocessing.py    # Task 1: Cleans and normalizes data
│   ├── sentiment_analysis.py # Task 2: BERT Sentiment & Theme extraction
│   ├── db_loader.py        # Task 3: Loads data to PostgreSQL
│   └── visualize.py        # Task 4: Generates insights & plots
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
    Ensure you have Docker installed. Create a `.env` file with your credentials (see `.env.example`).

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

**Objective:** Design and implement a relational database to store processed data.

### Database Schema
The project uses a normalized schema hosted via Docker.

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

**Execution:**
```bash
# 1. Start Container
docker-compose up -d

# 2. Run Loader Script
python scripts/db_loader.py
```

---

## 📊 Task 4: Visualization & Insights

**Objective:** Derive insights and visualize results for stakeholders.

### Key Visuals Generated
1.  **Sentiment Distribution:** Stacked bar chart comparing positive vs. negative sentiment per bank.
2.  **Pain Point Analysis:** Breakdown of negative themes (e.g., identifying "App Stability" as a major issue for BOA).
3.  **Word Cloud:** Visual representation of common terms in negative reviews.

**Execution:**
```bash
python scripts/visualize.py
```
*Outputs saved to: `reports/figures/`*

---

## 🧪 Testing
This project uses GitHub Actions for CI/CD. To run tests locally:
```bash
pytest
```

## 📝 Author
**Adem M**  
10 Academy AI  
Date: Dec 2025
```
