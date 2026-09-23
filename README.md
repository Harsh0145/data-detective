# 🕵️ Data Detective

**Upload your data. We'll investigate it.**

Data Detective is a Python + Streamlit portfolio project that automatically profiles a CSV dataset, investigates data quality, statistics, potential outliers, correlations, trends, categories, and generates a concise data story.

## 🚀 Live Demo

Add the Streamlit deployment URL here after deployment.

## Features

- CSV upload and validation
- Dataset profile: rows, columns, types, missing cells, duplicates
- Numeric, categorical and date detection
- Potential target-variable detection
- Data-quality investigation
- Descriptive statistics
- IQR-based potential outlier detection
- Correlation analysis
- Date-based trend analysis
- Category-level aggregation
- Automatically generated findings
- Actionable recommendations
- Raw-data preview
- Automated pytest tests

## Tech Stack

Python · Pandas · NumPy · Streamlit · Pytest

## Architecture

CSV → Data Inspection → Dataset Profile → Data Quality → Statistics → Relationships → Anomalies → Trends/Categories → Findings → Recommendations

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

Run tests:

```bash
pytest
```

## Analytical notes

The project uses transparent, deterministic rules. Potential outliers are identified with the IQR rule and should be investigated rather than automatically treated as errors. Correlations describe association and do not establish causation.

## License

MIT
