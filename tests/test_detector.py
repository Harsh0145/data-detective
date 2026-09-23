import pandas as pd
from src.detector import analyze_dataset, detect_anomalies, find_correlations, category_summary


def sample_df():
    return pd.DataFrame({"Date": pd.date_range("2026-01-01", periods=6), "Region": ["North","South","North","South","North","South"], "Revenue": [100,110,105,120,115,500], "Profit": [20,25,22,28,27,150]})


def test_profile():
    p=analyze_dataset(sample_df()); assert p["rows"]==6; assert p["columns"]==4; assert "Revenue" in p["numeric"]; assert p["date"]=="Date"

def test_anomalies():
    assert any(r["Variable"]=="Revenue" for r in detect_anomalies(sample_df()))

def test_correlations():
    assert find_correlations(sample_df())

def test_category_summary():
    result=category_summary(sample_df(),"Region","Revenue"); assert len(result)==2; assert "Total Revenue" in result.columns
