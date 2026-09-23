import streamlit as st
import pandas as pd

from src.detector import analyze_dataset, detect_anomalies, find_correlations, find_date_column, category_summary, numeric_summary, build_findings, build_recommendations

st.set_page_config(page_title="Data Detective", page_icon="🕵️", layout="wide")
st.title("🕵️ Data Detective")
st.caption("Upload your data. We’ll investigate it.")

uploaded = st.file_uploader("Upload a CSV file to investigate", type=["csv"])
if not uploaded:
    st.info("Start by uploading a CSV dataset.")
    st.markdown("""### What Data Detective investigates
- 📋 Dataset profile and column types
- 🧹 Missing values, duplicates and constant columns
- 📊 Descriptive statistics and distributions
- 🚨 Potential outliers using the IQR method
- 🔗 Numerical correlations
- 📅 Trends when a date column is detected
- 🏷️ Category-level patterns
- 💡 Automatically generated findings and recommendations

**Note:** Findings describe patterns in the uploaded data. Correlation does not imply causation, and outliers are flagged as potential anomalies rather than errors.
""")
    st.stop()

try:
    df = pd.read_csv(uploaded)
except Exception as exc:
    st.error(f"Could not read this CSV: {exc}")
    st.stop()

if df.empty or len(df.columns) == 0:
    st.error("The CSV appears to be empty.")
    st.stop()

profile = analyze_dataset(df)
anomalies = detect_anomalies(df)
correlations = find_correlations(df)
date_col = find_date_column(df)
findings = build_findings(df, profile, anomalies, correlations, date_col)
recommendations = build_recommendations(profile, anomalies)

st.success(f"Investigation loaded: {len(df):,} rows × {len(df.columns):,} columns")

st.header("📋 Dataset Profile")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{profile['rows']:,}")
c2.metric("Columns", f"{profile['columns']:,}")
c3.metric("Missing cells", f"{profile['missing_pct']:.1f}%")
c4.metric("Duplicate rows", f"{profile['duplicates']:,}")

left, right = st.columns(2)
with left:
    st.subheader("Variables")
    st.write("**Numeric:**", ", ".join(profile["numeric"]) or "None detected")
    st.write("**Categorical:**", ", ".join(profile["categorical"]) or "None detected")
    st.write("**Date:**", date_col or "None detected")
    st.write("**Potential target:**", profile["potential_target"] or "Not confidently detected")
with right:
    st.subheader("Detected issues")
    for issue in profile["issues"]:
        st.write(f"⚠️ {issue}")
    if not profile["issues"]:
        st.write("✅ No major structural issues detected.")

st.divider()
st.header("🧹 Data Quality")
if profile["column_quality"]:
    st.dataframe(pd.DataFrame(profile["column_quality"]), use_container_width=True, hide_index=True)
else:
    st.info("No column-level quality issues detected.")

st.divider()
st.header("📊 Statistical Investigation")
if profile["numeric"]:
    st.dataframe(numeric_summary(df, profile["numeric"]), use_container_width=True, hide_index=True)
    selected = st.selectbox("Inspect a numeric variable", profile["numeric"])
    st.bar_chart(df[selected].dropna().value_counts().sort_index().head(80))
else:
    st.info("No numeric columns were detected.")

st.divider()
st.header("🚨 Outlier Detective")
if anomalies:
    st.dataframe(pd.DataFrame(anomalies), use_container_width=True, hide_index=True)
else:
    st.success("No potential outliers were detected by the IQR rule.")

st.divider()
st.header("🔗 Relationship Detective")
if correlations:
    st.dataframe(pd.DataFrame(correlations), use_container_width=True, hide_index=True)
    st.caption("Correlation is a statistical association, not proof of causation.")
else:
    st.info("At least two suitable numeric columns are needed for correlation analysis.")

st.divider()
st.header("📅 Trend Detective")
if date_col and profile["numeric"]:
    trend = df[[date_col] + profile["numeric"]].copy()
    trend[date_col] = pd.to_datetime(trend[date_col], errors="coerce")
    trend = trend.dropna(subset=[date_col]).sort_values(date_col).set_index(date_col)
    if not trend.empty:
        target = profile["potential_target"] if profile["potential_target"] in profile["numeric"] else profile["numeric"][0]
        st.line_chart(trend[target].resample("ME").mean().dropna())
        st.caption(f"Monthly mean trend for **{target}**.")
    else:
        st.info("The detected date column could not be used for a numeric trend.")
else:
    st.info("No reliable date column was detected, so trend analysis is hidden.")

st.divider()
st.header("🏷️ Category Detective")
if profile["categorical"] and profile["numeric"]:
    cat = st.selectbox("Choose a category", profile["categorical"])
    value = st.selectbox("Measure", profile["numeric"])
    summary = category_summary(df, cat, value)
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.bar_chart(summary.set_index(cat)[f"Total {value}"].head(20))
else:
    st.info("Category analysis needs at least one categorical and one numeric variable.")

st.divider()
st.header("🕵️ Detective's Findings")
for finding in findings:
    st.write(f"- {finding}")
st.header("💡 Recommendations")
for recommendation in recommendations:
    st.write(f"- {recommendation}")

with st.expander("Preview uploaded data"):
    st.dataframe(df.head(100), use_container_width=True)

st.caption("Data Detective is an analytical portfolio tool. It does not claim causality and does not silently alter your original dataset.")
