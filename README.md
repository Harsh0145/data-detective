# 🕵️ Data Detective

**Upload your data. We'll investigate it.**

Data Detective is a Python + Streamlit portfolio project that automatically investigates CSV datasets and turns raw data into a clear analytical report.

It examines **data quality, statistics, potential outliers, correlations, trends, categories, findings, and recommendations** — all through a simple interactive dashboard.

## 🚀 Live Demo

**Live Demo:** https://data-detective-smvf7ogvskv4zjedaaybz6.streamlit.app/

**GitHub:** https://github.com/Harsh0145/data-detective

## 🔍 What Data Detective Investigates

* CSV upload and validation
* Dataset size and structure
* Numeric, categorical, and date variables
* Missing values
* Duplicate rows
* Constant and empty columns
* Potential target-variable detection
* Descriptive statistics
* Potential outliers using the IQR method
* Numerical correlations
* Date-based trends
* Category-level analysis
* Automatically generated findings
* Analytical recommendations
* Uploaded-data preview
* Automated tests with pytest

## 🧠 How It Works

```text
CSV Upload
    ↓
Data Inspection
    ↓
Dataset Profile
    ↓
Data Quality
    ↓
Statistics
    ↓
Relationships
    ↓
Anomaly Detection
    ↓
Trends & Categories
    ↓
Detective's Findings
    ↓
Recommendations
```

## 🛠️ Tech Stack

* Python
* Pandas
* NumPy
* Streamlit
* Pytest

## 📊 Key Analytical Methods

### Data Quality

Checks for:

* Missing values
* Duplicate rows
* Constant columns
* Completely empty columns

### Outlier Detection

Potential numerical outliers are detected using the **Interquartile Range (IQR)** rule.

Outliers are flagged for investigation rather than automatically removed.

### Correlation Analysis

The application calculates numerical correlations and identifies their:

* Strength
* Direction
* Correlation coefficient

> Correlation indicates statistical association and does not establish causation.

### Trend Analysis

When a reliable date/time column is detected, Data Detective can investigate how a numerical variable changes over time.

### Category Analysis

Categorical variables can be compared against numerical measures using:

* Record counts
* Averages
* Totals

## 💡 Why I Built This

Data analysis often begins with a messy CSV file and a simple question:

> **"What's actually going on in this data?"**

Data Detective automates the first stage of that investigation so analysts can quickly understand a dataset before moving into deeper analysis or machine-learning workflows.

## ▶️ Run Locally

Clone the repository:

```bash
git clone https://github.com/Harsh0145/data-detective.git
cd data-detective
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python -m streamlit run app.py
```

## 🧪 Run Tests

Run the automated test suite with:

```bash
pytest
```

The current test suite covers the core dataset profiling, anomaly detection, correlation analysis, and category analysis functions.

## 📁 Project Structure

```text
data-detective/
│
├── .streamlit/
│   └── config.toml
│
├── src/
│   ├── __init__.py
│   └── detector.py
│
├── tests/
│   └── test_detector.py
│
├── app.py
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## 📌 Analytical Notes

Data Detective uses transparent, deterministic rules to identify patterns in uploaded data.

The application does **not** silently modify the original dataset.

Potential outliers should be investigated in their business context rather than automatically treated as errors.

Correlation should be interpreted as association, not causation.

Automated findings are intended to support analysis, not replace domain knowledge or professional judgment.

## 📄 License

MIT License
