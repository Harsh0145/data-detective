import numpy as np
import pandas as pd


def _clean_columns(df):
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]
    return out


def find_date_column(df):
    for col in df.columns:
        name = str(col).lower()
        if any(k in name for k in ["date", "time", "month", "year"]):
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().mean() >= 0.70:
                return col
    for col in df.columns:
        if pd.api.types.is_object_dtype(df[col]):
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().mean() >= 0.90 and parsed.nunique(dropna=True) >= 3:
                return col
    return None


def _potential_target(df, numeric):
    keywords = ["target", "label", "sales", "revenue", "profit", "price", "amount", "score", "salary"]
    for col in numeric:
        if any(k in str(col).lower() for k in keywords):
            return col
    return numeric[0] if len(numeric) == 1 else None


def analyze_dataset(df):
    df = _clean_columns(df)
    numeric = df.select_dtypes(include=np.number).columns.tolist()
    date_col = find_date_column(df)
    categorical = [c for c in df.columns if c not in numeric and c != date_col]
    total_cells = max(df.shape[0] * df.shape[1], 1)
    missing = int(df.isna().sum().sum())
    missing_pct = missing / total_cells * 100
    duplicates = int(df.duplicated().sum())
    constant = [c for c in df.columns if df[c].nunique(dropna=False) <= 1]
    completely_empty = [c for c in df.columns if df[c].isna().all()]
    quality = []
    for col in df.columns:
        pct = float(df[col].isna().mean() * 100)
        if pct > 0:
            quality.append({"Column": col, "Missing %": round(pct, 2), "Unique values": int(df[col].nunique(dropna=True)), "Data type": str(df[col].dtype)})
    issues = []
    if missing_pct > 0: issues.append(f"{missing_pct:.1f}% of cells contain missing values")
    if duplicates: issues.append(f"{duplicates:,} duplicate rows")
    if constant: issues.append(f"{len(constant)} constant column(s)")
    if completely_empty: issues.append(f"{len(completely_empty)} completely empty column(s)")
    return {"rows": len(df), "columns": len(df.columns), "numeric": numeric, "categorical": categorical, "date": date_col, "missing_pct": missing_pct, "duplicates": duplicates, "constant": constant, "empty": completely_empty, "potential_target": _potential_target(df, numeric), "column_quality": quality, "issues": issues}


def numeric_summary(df, numeric):
    rows = []
    for col in numeric:
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        if s.empty: continue
        rows.append({"Variable": col, "Mean": round(float(s.mean()), 3), "Median": round(float(s.median()), 3), "Min": round(float(s.min()), 3), "Q1": round(float(s.quantile(.25)), 3), "Q3": round(float(s.quantile(.75)), 3), "Max": round(float(s.max()), 3), "Std Dev": round(float(s.std()) if len(s)>1 else 0, 3), "Skewness": round(float(s.skew()) if len(s)>2 else 0, 3)})
    return pd.DataFrame(rows)


def detect_anomalies(df):
    rows = []
    for col in df.select_dtypes(include=np.number).columns:
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        if len(s) < 4 or s.nunique() < 4: continue
        q1, q3 = s.quantile(.25), s.quantile(.75)
        iqr = q3 - q1
        if iqr == 0: continue
        lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
        mask = (s < lower) | (s > upper)
        count = int(mask.sum())
        if count:
            rows.append({"Variable": col, "Potential outliers": count, "Outlier %": round(count/len(s)*100,2), "Lower bound": round(float(lower),3), "Upper bound": round(float(upper),3), "Highest value": round(float(s.max()),3), "Lowest value": round(float(s.min()),3)})
    return rows


def find_correlations(df):
    numeric = df.select_dtypes(include=np.number)
    if numeric.shape[1] < 2: return []
    corr = numeric.corr(numeric_only=True)
    rows=[]; cols=corr.columns.tolist()
    for i in range(len(cols)):
        for j in range(i+1,len(cols)):
            value=corr.iloc[i,j]
            if pd.notna(value):
                rows.append({"Variable A":cols[i],"Variable B":cols[j],"Correlation":round(float(value),3),"Strength":"Strong" if abs(value)>=.70 else "Moderate" if abs(value)>=.40 else "Weak","Direction":"Positive" if value>0 else "Negative" if value<0 else "None"})
    return sorted(rows,key=lambda x:abs(x["Correlation"]),reverse=True)[:10]


def category_summary(df, category, value):
    temp=df[[category,value]].copy(); temp[value]=pd.to_numeric(temp[value],errors="coerce")
    result=temp.dropna(subset=[category]).groupby(category)[value].agg(["count","mean","sum"]).reset_index().sort_values("sum",ascending=False)
    result.columns=[category,"Records",f"Average {value}",f"Total {value}"]
    return result.head(20)


def build_findings(df, profile, anomalies, correlations, date_col):
    findings=[]
    if profile["missing_pct"]>0: findings.append(f"⚠️ Missing data affects {profile['missing_pct']:.1f}% of all cells.")
    if profile["duplicates"]: findings.append(f"⚠️ {profile['duplicates']:,} duplicate rows may need review.")
    if profile["constant"]: findings.append(f"⚠️ Constant columns detected: {', '.join(profile['constant'][:5])}.")
    if anomalies:
        top=max(anomalies,key=lambda x:x["Potential outliers"]); findings.append(f"🚨 {top['Variable']} has {top['Potential outliers']:,} potential outlier(s) by the IQR rule.")
    if correlations:
        top=correlations[0]; findings.append(f"🔗 {top['Variable A']} and {top['Variable B']} show a {top['Strength'].lower()} {top['Direction'].lower()} correlation ({top['Correlation']:.2f}).")
    if date_col: findings.append(f"📅 A usable date/time field was detected: {date_col}. Trend analysis is available.")
    return findings or ["🟢 No major automated issues or relationships were detected."]


def build_recommendations(profile, anomalies):
    recs=[]
    if profile["missing_pct"]>0: recs.append("Review missing values before modeling or drawing conclusions; choose imputation or removal based on business context.")
    if profile["duplicates"]: recs.append("Inspect duplicate rows and determine whether they are genuine repeated events or accidental duplicates.")
    if profile["constant"]: recs.append("Consider removing constant columns from analytical or machine-learning workflows.")
    if anomalies: recs.append("Investigate potential outliers individually; do not automatically delete them.")
    return recs or ["The dataset has no major structural issue detected by the current rules. Continue with domain-specific validation."]
