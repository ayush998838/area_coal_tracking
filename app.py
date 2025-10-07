import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import base64
import pdfplumber
try:
    import tabula  # requires Java; not available on Streamlit Cloud
    TABULA_AVAILABLE = True
except Exception:
    TABULA_AVAILABLE = False
import io

# Page configuration
st.set_page_config(
    page_title="Bharat Coking Coal Limited - Production Analytics",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Futuristic CSS with animations and 3D effects
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --dark-bg: #0a0a0a;
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --neon-blue: #00d4ff;
        --neon-purple: #8b5cf6;
        --neon-green: #10b981;
        --neon-orange: #f59e0b;
    }
    
    * {
        font-family: 'Rajdhani', sans-serif;
    }
    
    .main {
        background: radial-gradient(ellipse at center, #1a1a2e 0%, #0a0a0a 70%);
        color: #ffffff;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }
    
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Futuristic Header */
    .futuristic-header {
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .futuristic-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--neon-blue), transparent);
        animation: scan 3s infinite;
    }
    
    @keyframes scan {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        z-index: 2;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        transition: all 0.3s ease;
        padding: 0.5rem;
        border-radius: 15px;
    }
    
    .logo-section:hover {
        background: rgba(0, 212, 255, 0.1);
        transform: scale(1.02);
    }
    
    .logo-3d {
        transform: perspective(1000px) rotateY(-15deg);
        transition: all 0.3s ease;
        filter: drop-shadow(0 0 20px var(--neon-blue));
    }
    
    .logo-3d:hover {
        transform: perspective(1000px) rotateY(0deg) scale(1.1);
        filter: drop-shadow(0 0 30px var(--neon-blue));
    }
    
    .company-info h1 {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        font-weight: 900;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    .company-info p {
        color: var(--neon-blue);
        margin: 0;
        font-size: 1rem;
        font-weight: 500;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(102, 126, 234, 0.5); }
        to { text-shadow: 0 0 30px rgba(102, 126, 234, 0.8); }
    }
    
    /* Navigation */
    .nav-container {
        display: flex;
        gap: 0.5rem;
    }
    
    .nav-button {
        padding: 0.75rem 1.5rem;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 15px;
        color: #ffffff;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .nav-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .nav-button:hover {
        background: var(--primary-gradient);
        border-color: var(--neon-blue);
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
    
    .nav-button:hover::before {
        left: 100%;
    }
    
    .nav-button.active {
        background: var(--accent-gradient);
        border-color: var(--neon-blue);
        box-shadow: 0 0 20px rgba(79, 172, 254, 0.5);
    }
    
    /* Cards and Components */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 15px 40px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: var(--neon-blue);
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--neon-blue), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .glass-card:hover::before {
        opacity: 1;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary-gradient);
        color: #ffffff;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.5);
        background: var(--secondary-gradient);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:active::before {
        width: 300px;
        height: 300px;
    }
    
    /* Form Elements */
    .stSelectbox > div > div {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 15px;
        color: #ffffff;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--neon-blue);
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
    }
    
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 15px;
        color: #ffffff;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--neon-blue);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
        outline: none;
    }
    
    /* Metrics */
    .metric-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card:hover {
        transform: translateY(-5px) rotateX(5deg);
        border-color: var(--neon-green);
        box-shadow: 0 15px 40px rgba(16, 185, 129, 0.3);
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: var(--accent-gradient);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover::after {
        transform: scaleX(1);
    }
    
    /* Issue Indicators */
    .issue-land {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
        border-left: 4px solid var(--neon-green);
        padding: 0.75rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .issue-land::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.3), transparent);
        animation: slide 2s infinite;
    }
    
    .issue-climate {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1));
        border-left: 4px solid var(--neon-orange);
        padding: 0.75rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .issue-climate::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(245, 158, 11, 0.3), transparent);
        animation: slide 2s infinite;
    }
    
    .issue-custom {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(139, 92, 246, 0.1));
        border-left: 4px solid var(--neon-purple);
        padding: 0.75rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .issue-custom::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.3), transparent);
        animation: slide 2s infinite;
    }
    
    @keyframes slide {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Animations */
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in-left {
        animation: slideInLeft 0.8s ease-out;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .slide-in-right {
        animation: slideInRight 0.8s ease-out;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Hide Streamlit default elements */
    .stApp > header {
        display: none;
    }
    
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'areas_data' not in st.session_state:
    st.session_state.areas_data = {}
if 'num_areas' not in st.session_state:
    st.session_state.num_areas = 0
if 'time_duration' not in st.session_state:
    st.session_state.time_duration = 0
if 'setup_complete' not in st.session_state:
    st.session_state.setup_complete = False
if 'months' not in st.session_state:
    st.session_state.months = []
if 'start_date' not in st.session_state:
    st.session_state.start_date = None
if 'end_date' not in st.session_state:
    st.session_state.end_date = None
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'area_names' not in st.session_state:
    st.session_state.area_names = []
if 'uploaded_area_df' not in st.session_state:
    st.session_state.uploaded_area_df = None
if 'uploaded_other_dfs' not in st.session_state:
    st.session_state.uploaded_other_dfs = []

def _coerce_numeric_series(series: pd.Series) -> pd.Series:
    """Coerce a series to numeric by stripping non numeric chars (keeps digits, dot, minus)."""
    try:
        cleaned = series.astype(str).str.replace(",", "").str.replace("\u2212", "-")
        cleaned = cleaned.str.replace(r"[^0-9.\-]", "", regex=True)
        return pd.to_numeric(cleaned, errors='coerce')
    except Exception:
        return pd.to_numeric(series, errors='coerce')

def _coerce_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    try:
        out = df.copy()
        for col in out.columns:
            coerced = _coerce_numeric_series(out[col])
            # adopt if we got any numbers
            if coerced.notna().sum() >= max(2, int(0.3 * len(out))):
                out[col] = coerced
        return out
    except Exception:
        return df

def _read_table_file_to_dfs(uploaded_file):
    """Read an uploaded file (PDF/Excel/CSV) and return list of DataFrames.

    - PDF: extract tables with pdfplumber; returns each table as a DataFrame
    - Excel: read first sheet to a single DataFrame
    - CSV: read to a single DataFrame
    """
    dfs = []
    try:
        if uploaded_file is None:
            return dfs
        filename = uploaded_file.name.lower()
        mime = uploaded_file.type or ""
        # Excel
        if filename.endswith((".xlsx", ".xls")) or "excel" in mime:
            try:
                df = pd.read_excel(uploaded_file)
                dfs.append(df)
                return dfs
            except Exception:
                pass
        # CSV
        if filename.endswith(".csv") or "csv" in mime:
            try:
                df = pd.read_csv(uploaded_file)
                dfs.append(df)
                return dfs
            except Exception:
                pass
        # PDF via pdfplumber
        if filename.endswith(".pdf") or "pdf" in mime:
            try:
                pdf_bytes = uploaded_file.getvalue()
            except Exception:
                pdf_bytes = uploaded_file.read()
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables or []:
                        if not table or len(table) == 0:
                            continue
                        # First row as header if looks like header; else create generic headers
                        header = table[0]
                        data_rows = table[1:] if len(table) > 1 else []
                        # If any header cell is None or empty, make generic names
                        if any((h is None or str(h).strip() == "") for h in header):
                            cols = [f"col_{i+1}" for i in range(len(header))]
                        else:
                            cols = [str(h).strip() for h in header]
                        df = pd.DataFrame(data_rows, columns=cols)
                        # Attempt numeric conversion where possible (coerce to better detect numerics)
                        df = _coerce_numeric_columns(df)
                        dfs.append(df)
            return dfs
    except Exception:
        return dfs
    return dfs

def _extract_area_value_from_pdf_text(pdf_bytes: bytes) -> pd.DataFrame | None:
    """Fallback: parse area/value pairs by scanning PDF text lines.

    Returns a DataFrame with columns ['Area', 'Value'] or None if nothing parsed.
    """
    try:
        records = []
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                for raw_line in text.splitlines():
                    line = " ".join(raw_line.split())
                    if not line or len(line) < 3:
                        continue
                    # Heuristic: find a trailing number (possibly with commas/decimals) and optional unit
                    # Example: "Katras Area 3,500,000" or "Katras Area 3.5"
                    import re
                    m = re.search(r"(.+?)\s+([0-9][0-9,\.]*)(?:\s*(?:MT|Mt|mt|T|Tonnes|Million\s*Tonnes|MMT|mmt|Lakh|lakh)\b)?$", line)
                    if not m:
                        continue
                    area = m.group(1).strip().strip(':')
                    value_str = m.group(2).replace(",", "").strip()
                    # Filter out obvious headers, but keep domain words like coal/production
                    if any(k in area.lower() for k in ["government", "ministry", "india", "company", "limited", "page", "year", "report", "annexure", "appendix", "url", "http"]):
                        continue
                    # Keep moderately sized names
                    if len(area) < 2 or len(area) > 60:
                        continue
                    try:
                        value = float(value_str)
                    except Exception:
                        continue
                    if value <= 0:
                        continue
                    records.append((area, value))
        if records:
            df = pd.DataFrame(records, columns=["Area", "Value"])
            # Deduplicate by area keeping the max value if duplicates
            df = df.groupby("Area", as_index=False)["Value"].max()
            return df
    except Exception:
        return None
    return None

def _guess_area_and_value_columns(df: pd.DataFrame):
    """Heuristically guess area/name column and value column from a DataFrame."""
    cols_lower = {c: str(c).lower() for c in df.columns}
    area_col = None
    value_col = None
    # Find area-like column
    for c, lc in cols_lower.items():
        if any(k in lc for k in ["area", "colliery", "mine", "project", "field"]):
            area_col = c
            break
    # Find numeric value-like column
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if numeric_cols:
        # Prefer coal/production/output named columns
        preferred = [c for c in numeric_cols if any(k in cols_lower[c] for k in ["coal", "production", "output", "target", "actual"]) ]
        value_col = preferred[0] if len(preferred) > 0 else numeric_cols[0]
    # If area not found, try first non-numeric column
    if area_col is None:
        non_num = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]
        area_col = non_num[0] if non_num else (df.columns[0] if len(df.columns) > 0 else None)
    return area_col, value_col

def _plot_area_line_chart(df: pd.DataFrame, area_col: str, value_col: str, title_suffix: str = ""):
    """Render a single line chart for area vs value."""
    try:
        display_df = df[[area_col, value_col]].dropna()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=display_df[area_col].astype(str).tolist(),
            y=pd.to_numeric(display_df[value_col], errors='coerce').tolist(),
            mode='lines+markers',
            name='Coal Output',
            line=dict(color='#10b981', width=4),
            marker=dict(size=10, color='#10b981', line=dict(width=1, color='#ffffff')),
            hovertemplate='<b>%{x}</b><br>Output: %{y:,.0f} T<extra></extra>'
        ))
        fig.update_layout(
            title=f'Area-wise Coal Production {title_suffix}'.strip(),
            xaxis_title='Area',
            yaxis_title='Coal Output (Tonnes)',
            template='plotly_dark',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as _:
        st.warning("Could not render line chart for the uploaded area-wise document.")

def _fallback_text_parse_table(pdf_bytes: bytes) -> list[pd.DataFrame]:
    """Parse generic label/value pairs from PDF text to best-effort DataFrame(s)."""
    try:
        import re
        tables = []
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            lines = []
            for page in pdf.pages:
                t = page.extract_text() or ""
                lines.extend(t.splitlines())
        pairs = []
        for raw in lines:
            line = " ".join(raw.split())
            m = re.search(r"(.+?)\s+([0-9][0-9,\.]*)(?:\s*(?:%|MT|Mt|mt|T|Tonnes|MMT|Lakh)\b)?$", line)
            if not m:
                continue
            label = m.group(1).strip().strip(':')
            value = _coerce_numeric_series(pd.Series([m.group(2)])).iloc[0]
            if pd.notna(value):
                pairs.append((label, float(value)))
        if pairs:
            df = pd.DataFrame(pairs, columns=["Label", "Value"]).groupby("Label", as_index=False)["Value"].max()
            tables.append(df)
        return tables
    except Exception:
        return []

def _auto_plot_other(df: pd.DataFrame, title: str | None = None):
    """Attempt a reasonable visualization for generic tables.

    Priority:
    1) If one categorical column and >=1 numeric columns: plot line(s) by category on x-axis
    2) Else if >=2 numeric: plot first numeric as line over index
    3) Always show table preview
    """
    try:
        # Normalize possible numeric strings to numeric
        for col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                coerced = pd.to_numeric(df[col].astype(str).str.replace(",", "").str.replace("\u2212", "-"), errors='coerce')
                # If many values converted, keep it
                if coerced.notna().sum() >= max(2, int(0.5 * len(df))):
                    df[col] = coerced

        st.dataframe(df, use_container_width=True)

        numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        cat_cols = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]

        plot_title = title or ""

        if cat_cols and numeric_cols:
            # Heuristic 1: wide format -> one categorical x and multiple numeric series
            if len(cat_cols) == 1 and len(numeric_cols) >= 1:
                x_col = cat_cols[0]
                # Try to sort x smartly (date-like or numeric)
                try:
                    x_parsed = pd.to_datetime(df[x_col], errors='coerce')
                    if x_parsed.notna().any():
                        df = df.assign(_x=x_parsed.fillna(df[x_col].astype(str)))
                        x_values = df['_x']
                    else:
                        x_values = df[x_col]
                except Exception:
                    # numeric sort fallback
                    x_values = df[x_col]

                fig = go.Figure()
                palette = ['#10b981', '#f59e0b', '#ef4444', '#3b82f6', '#8b5cf6', '#22d3ee', '#84cc16', '#e11d48']
                for idx, y_col in enumerate(numeric_cols):
                    color = palette[idx % len(palette)]
                    fig.add_trace(go.Scatter(
                        x=x_values.astype(str),
                        y=df[y_col],
                        mode='lines+markers',
                        name=str(y_col),
                        line=dict(color=color)
                    ))
                fig.update_layout(
                    template='plotly_dark',
                    xaxis_title=str(x_col),
                    yaxis_title='Value',
                    height=500,
                    title=plot_title
                )
                st.plotly_chart(fig, use_container_width=True)
            # Heuristic 2: long format -> two categoricals + one numeric
            elif len(cat_cols) >= 2 and len(numeric_cols) == 1:
                # Choose x as the categorical with more unique values; other as series name
                x_col = max(cat_cols, key=lambda c: df[c].nunique(dropna=True))
                series_col = [c for c in cat_cols if c != x_col][0]
                y_col = numeric_cols[0]
                fig = go.Figure()
                palette = ['#10b981', '#f59e0b', '#ef4444', '#3b82f6', '#8b5cf6', '#22d3ee', '#84cc16', '#e11d48']
                for idx, (series_value, gdf) in enumerate(df.groupby(series_col)):
                    color = palette[idx % len(palette)]
                    # preserve order; try date parsing for x
                    try:
                        x_vals = pd.to_datetime(gdf[x_col], errors='coerce')
                        if x_vals.notna().any():
                            x_vals = x_vals.fillna(gdf[x_col].astype(str))
                        else:
                            x_vals = gdf[x_col].astype(str)
                    except Exception:
                        x_vals = gdf[x_col].astype(str)
                    fig.add_trace(go.Scatter(
                        x=x_vals,
                        y=gdf[y_col],
                        mode='lines+markers',
                        name=str(series_value),
                        line=dict(color=color)
                    ))
                fig.update_layout(
                    template='plotly_dark',
                    xaxis_title=str(x_col),
                    yaxis_title=str(y_col),
                    height=520,
                    title=plot_title
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Fallback to first categorical as x with multi numeric series if any
                x_col = cat_cols[0]
                fig = go.Figure()
                for y_col in numeric_cols:
                    fig.add_trace(go.Scatter(x=df[x_col].astype(str), y=df[y_col], mode='lines+markers', name=str(y_col)))
                fig.update_layout(template='plotly_dark', xaxis_title=str(x_col), yaxis_title='Value', height=500, title=plot_title)
                st.plotly_chart(fig, use_container_width=True)
        elif len(numeric_cols) >= 1:
            y_col = numeric_cols[0]
            fig = go.Figure(go.Scatter(y=df[y_col], mode='lines+markers', line=dict(color='#f59e0b'), name=str(y_col)))
            fig.update_layout(template='plotly_dark', xaxis_title='Index', yaxis_title=str(y_col), height=450, title=plot_title)
            st.plotly_chart(fig, use_container_width=True)
    except Exception as _:
        st.info("Preview shown. No suitable automatic chart detected.")

def initialize_areas():
    """Initialize area data structure"""
    st.session_state.areas_data = {}
    for i in range(1, st.session_state.num_areas + 1):
        area_name = f"Area {i}"
        if st.session_state.area_names and i-1 < len(st.session_state.area_names):
            area_name = st.session_state.area_names[i-1]
        st.session_state.areas_data[area_name] = {
            'expected': {},
            'actual': {},
            'issues': {}
        }

def generate_months():
    """Generate list of months based on date range"""
    months = []
    try:
        if (hasattr(st.session_state, 'start_date') and hasattr(st.session_state, 'end_date') 
            and st.session_state.start_date is not None and st.session_state.end_date is not None):
            
            start_date = st.session_state.start_date
            end_date = st.session_state.end_date
            
            # Generate months between start and end date
            current_date = datetime(start_date.year, start_date.month, 1)
            end_datetime = datetime(end_date.year, end_date.month, 1)
            
            while current_date <= end_datetime:
                month_str = current_date.strftime("%B %Y")
                months.append(month_str)
                # Move to next month
                if current_date.month == 12:
                    current_date = current_date.replace(year=current_date.year + 1, month=1)
                else:
                    current_date = current_date.replace(month=current_date.month + 1)
        else:
            # Fallback to old method if dates not set
            current_date = datetime.now().replace(day=1)
            for i in range(max(1, st.session_state.time_duration)):
                month_date = current_date + timedelta(days=30*i)
                month_str = month_date.strftime("%B %Y")
                months.append(month_str)
    except Exception as e:
        # Final fallback
        months = [datetime.now().strftime("%B %Y")]

    st.session_state.months = months

def display_header(page_title="", current_page=""):
    """Display futuristic header with logo and navigation"""
    logo_base64 = get_image_base64()
    theme_toggle_label = "🌙 Dark" if st.session_state.theme == "light" else "☀️ Light"
    st.markdown(f"""
    <div class="futuristic-header fade-in">
        <div class="header-content">
            <div class="logo-section">
                <img src="data:image/jpeg;base64,{logo_base64}" class="logo-3d" style="height:80px; width:auto;" />
                <div class="company-info">
                    <h1>Bharat Coking Coal Limited</h1>
                    <p>Production Analytics Portal</p>
                </div>
            </div>
            <div class="nav-container">
                <a href="?page=setup" class="nav-button {'active' if current_page == 'setup' else ''}">🚀 Setup</a>
                <a href="?page=data" class="nav-button {'active' if current_page == 'data' else ''}">📊 Data Entry</a>
                <a href="?page=analytics" class="nav-button {'active' if current_page == 'analytics' else ''}">📈 Analytics</a>
                <a href="?page=dashboard" class="nav-button {'active' if current_page == 'dashboard' else ''}">🏭 Dashboard</a>
                <button id="theme-toggle" class="nav-button" style="margin-left: 10px;">{theme_toggle_label}</button>
            </div>
        </div>
    </div>
    <script>
    const btn = window.parent.document.getElementById("theme-toggle");
    if(btn) {{
        btn.onclick = () => {{
            window.parent.postMessage({{type: "toggle-theme"}}, "*");
        }};
    }}
    </script>
""", unsafe_allow_html=True)

def get_image_base64():
    """Convert image to base64 for embedding"""
    import base64
    try:
        with open("BCCL_LOGO-6.jpeg", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

def enable_pwa():
    """Inject a manifest and register a simple service worker to enable PWA install/offline."""
    try:
        logo_b64 = get_image_base64()
    except Exception:
        logo_b64 = ""
    manifest = {
        "name": "Bharat Coking Coal Limited - Production Analytics",
        "short_name": "BCCL Analytics",
        "start_url": ".",
        "display": "standalone",
        "background_color": "#0a0a0a",
        "theme_color": "#0a0a0a",
        "icons": [
            {
                "src": f"data:image/jpeg;base64,{logo_b64}",
                "sizes": "256x256",
                "type": "image/jpeg"
            }
        ]
    }
    import base64 as _b64
    manifest_b64 = _b64.b64encode(json.dumps(manifest).encode()).decode()
    theme_color = manifest.get("theme_color")
    script = """
    <script>
    try {
      if (!window.__pwa_initialized) {
        window.__pwa_initialized = true;
        const head = document.head || document.getElementsByTagName('head')[0];
        // Inject manifest from base64 to avoid template escaping issues
        const manifestJSON = JSON.parse(atob('%s'));
        const manifestBlob = new Blob([JSON.stringify(manifestJSON)], {type: 'application/manifest+json'});
        const manifestURL = URL.createObjectURL(manifestBlob);
        const link = document.createElement('link');
        link.setAttribute('rel','manifest');
        link.setAttribute('href', manifestURL);
        head.appendChild(link);
        // Theme color meta
        const meta = document.createElement('meta');
        meta.setAttribute('name','theme-color');
        meta.setAttribute('content', '%s');
        head.appendChild(meta);
        // Register service worker (network-first, cache fallback)
        if ('serviceWorker' in navigator) {
          const swCode = "self.addEventListener('install', e => {self.skipWaiting();});\n"+
                         "self.addEventListener('activate', e => {self.clients.claim();});\n"+
                         "self.addEventListener('fetch', e => {\n  e.respondWith((async () => {\n    try {\n      return await fetch(e.request);\n    } catch (err) {\n      const cache = await caches.open('offline-cache-v1');\n      const cached = await cache.match(e.request);\n      return cached || Response.error();\n    }\n  })());\n});";
          const blob = new Blob([swCode], {type:'text/javascript'});
          const swURL = URL.createObjectURL(blob);
          navigator.serviceWorker.register(swURL).catch(console.error);
        }
      }
    } catch(e) { console.warn('PWA init failed', e); }
    </script>
    """ % (manifest_b64, theme_color)
    st.markdown(script, unsafe_allow_html=True)

def create_header_with_logo():
    """Create header with clickable BCCL logo"""
    logo_base64 = get_image_base64()
    st.markdown(f"""
    <div class="futuristic-header fade-in">
        <div class="header-content">
            <div class="logo-section" style="cursor: pointer;" onclick="window.location.href='?page=setup'">
                <img src="data:image/jpeg;base64,{logo_base64}" class="logo-3d" style="height:120px; width:auto; transition: all 0.3s ease;" />
                <div class="company-info">
                    <h1>Bharat Coking Coal Limited</h1>
                    <p>Production Analytics Portal</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_setup_form():
    """Create initial setup form"""
    create_header_with_logo()
    
    st.markdown("""
    <div class="glass-card fade-in">
        <h2 style="color: var(--neon-blue); margin-bottom: 1.5rem; font-family: 'Orbitron', monospace;">
            🚀 System Initialization
        </h2>
        <p style="color: #cccccc; margin-bottom: 2rem;">
            Configure your production tracking system by setting up the number of mining areas and time period.
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card slide-in-left">
            <h3 style="color: var(--neon-green); margin-bottom: 1rem;">📍 Mining Areas</h3>
        """, unsafe_allow_html=True)
        st.session_state.num_areas = st.number_input(
            "Number of Areas",
            min_value=1,
            max_value=20,
            value=3,
            help="Enter the number of mining areas to track"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card slide-in-right">
            <h3 style="color: var(--neon-orange); margin-bottom: 1rem;">📅 Time Period</h3>
        """, unsafe_allow_html=True)
        
        # Date range selection
        col_start, col_end = st.columns(2)
        
        with col_start:
            st.session_state.start_date = st.date_input(
                "Start Date",
                value=datetime.now().replace(day=1),  # First day of current month
                help="Select the start date for tracking"
            )
        
        with col_end:
            st.session_state.end_date = st.date_input(
                "End Date",
                value=datetime.now().replace(day=1) + timedelta(days=365),  # One year from start
                help="Select the end date for tracking"
            )
        
        # Calculate duration automatically
        if st.session_state.start_date and st.session_state.end_date:
            duration_days = (st.session_state.end_date - st.session_state.start_date).days
            st.session_state.time_duration = max(1, duration_days // 30)  # Convert to months
            
            st.markdown(f"""
            <div style="background: rgba(79, 172, 254, 0.2); padding: 0.5rem; border-radius: 8px; margin-top: 0.5rem;">
                <p style="color: var(--neon-blue); margin: 0; font-size: 0.9rem;">
                    📊 Duration: {st.session_state.time_duration} months ({duration_days} days)
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Document uploads
    st.markdown("""
    <div class="glass-card fade-in">
        <h3 style="color: var(--neon-blue); margin-bottom: 1rem; font-family: 'Orbitron', monospace;">📂 Document Uploads</h3>
        <p style="color: #cccccc; margin-bottom: 1.5rem;">Upload official documents to auto-ingest data and visualize.</p>
    """, unsafe_allow_html=True)

    up_col1, up_col2 = st.columns(2)

    with up_col1:
        st.markdown("""
        <div class="metric-card slide-in-left">
            <h4 style="color: var(--neon-green); margin-bottom: 0.5rem;">Area-wise Coal Production</h4>
            <p style="color:#aaaaaa; margin:0 0 0.5rem 0; font-size: 0.9rem;">e.g., Area name + coal output. Example: Area-wise_coal_production_target_2024-25(45 MT).pdf</p>
        """, unsafe_allow_html=True)
        area_file = st.file_uploader(
            "Upload Area-wise Coal Production (PDF/Excel/CSV)",
            type=["pdf", "xlsx", "xls", "csv"],
            key="upload_area_wise",
        )
        if area_file is not None:
            with st.spinner("Parsing area-wise document..."):
                dfs = _read_table_file_to_dfs(area_file)
                best_df = None
                best_pair = (None, None)
                for df in dfs:
                    if df is None or df.empty:
                        continue
                    area_col, value_col = _guess_area_and_value_columns(df)
                    if area_col is not None and value_col is not None:
                        best_df = df
                        best_pair = (area_col, value_col)
                        break
                # If no table worked, fallback to text extraction for PDFs
                if best_df is None and area_file.name.lower().endswith('.pdf'):
                    try:
                        pdf_bytes = area_file.getvalue()
                    except Exception:
                        pdf_bytes = area_file.read()
                    text_df = _extract_area_value_from_pdf_text(pdf_bytes)
                    if text_df is not None and not text_df.empty:
                        best_df = text_df
                        best_pair = ("Area", "Value")
                if best_df is not None:
                    st.session_state.uploaded_area_df = best_df
                    st.markdown("<div style=\"margin: 0.5rem 0; color:#cccccc;\">Detected columns: <b>{}</b> (area), <b>{}</b> (value)</div>".format(best_pair[0], best_pair[1]), unsafe_allow_html=True)
                    _plot_area_line_chart(best_df, best_pair[0], best_pair[1], title_suffix=f"— {area_file.name}")
                    with st.expander("Preview parsed table", expanded=False):
                        st.dataframe(best_df, use_container_width=True)
                else:
                    st.warning("No suitable area/value columns found in the uploaded file.")
        st.markdown("</div>", unsafe_allow_html=True)

    with up_col2:
        st.markdown("""
        <div class="metric-card slide-in-right">
            <h4 style="color: var(--neon-orange); margin-bottom: 0.5rem;">Other Documents</h4>
            <p style="color:#aaaaaa; margin:0 0 0.5rem 0; font-size: 0.9rem;">e.g., Coalfield_wise_Coal_Production300823.pdf and similar. Multiple files supported.</p>
        """, unsafe_allow_html=True)
        other_files = st.file_uploader(
            "Upload Other Documents (PDF/Excel/CSV)",
            type=["pdf", "xlsx", "xls", "csv"],
            key="upload_other_docs",
            accept_multiple_files=True,
        )
        if other_files:
            st.session_state.uploaded_other_dfs = []
            for f in other_files:
                with st.spinner(f"Parsing {f.name}..."):
                    dfs = _read_table_file_to_dfs(f)
                    # Fallback to text pairs if no tables
                    if (not dfs) and f.name.lower().endswith('.pdf'):
                        try:
                            pdf_bytes = f.getvalue()
                        except Exception:
                            pdf_bytes = f.read()
                        dfs = _fallback_text_parse_table(pdf_bytes)
                    for idx, df in enumerate(dfs or []):
                        if df is None or df.empty:
                            continue
                        df = _coerce_numeric_columns(df)
                        st.session_state.uploaded_other_dfs.append({"name": f"{f.name} [table {idx+1}]", "df": df})
            if st.session_state.uploaded_other_dfs:
                for item in st.session_state.uploaded_other_dfs:
                    with st.expander(item["name"], expanded=False):
                        _auto_plot_other(item["df"], title=item["name"])
            else:
                st.info("No tables detected in uploaded documents.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card fade-in" style="text-align: center; margin-top: 2rem;">
        <p style="color: #ffffff; margin-bottom: 1rem;">
            Ready to initialize your production tracking system?
        </p>
    """, unsafe_allow_html=True)
    
    # Validation before initialization
    if st.session_state.num_areas <= 0:
        st.warning("⚠️ Please enter a valid number of areas (minimum 1)")
    elif st.session_state.time_duration <= 0:
        st.warning("⚠️ Please enter a valid time duration (minimum 1 month)")
    elif st.button("🚀 Initialize Production Tracking", type="primary"):
        try:
            with st.spinner("Initializing system..."):
                initialize_areas()
                generate_months()
                st.session_state.setup_complete = True
                
                st.success("✅ System initialized successfully!")
                st.balloons()
                # Redirect to data entry page
                st.session_state.current_page = 'data'
                st.rerun()
        except Exception as e:
            st.error(f"❌ Error during initialization: {str(e)}")
            st.write("Please check your input values and try again.")
    
    st.markdown("</div>", unsafe_allow_html=True)

def create_area_data_entry():
    """Create data entry interface for each area"""
    create_header_with_logo()
    
    st.markdown("""
    <div class="glass-card fade-in">
        <h2 style="color: var(--neon-blue); margin-bottom: 1.5rem; font-family: 'Orbitron', monospace;">
            📊 Production Data Entry
        </h2>
        <p style="color: #cccccc; margin-bottom: 2rem;">
            Enter monthly production data for each mining area with issue tracking.
        </p>
    """, unsafe_allow_html=True)
    
    # Month and Area selectors
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card slide-in-left">
            <h3 style="color: var(--neon-green); margin-bottom: 1rem;">📅 Select Month</h3>
        """, unsafe_allow_html=True)
        selected_month = st.selectbox("Select Month", st.session_state.months, key="month_selector")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card slide-in-right">
            <h3 style="color: var(--neon-orange); margin-bottom: 1rem;">📍 Select Area</h3>
        """, unsafe_allow_html=True)
        selected_area = st.selectbox("Select Area", list(st.session_state.areas_data.keys()), key="area_selector")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Data entry form
    st.markdown(f"""
    <div class="glass-card fade-in">
        <h3 style="color: var(--neon-blue); margin-bottom: 1.5rem; font-family: 'Orbitron', monospace;">
            {selected_area} - {selected_month}
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card slide-in-left">
            <h4 style="color: var(--neon-green); margin-bottom: 1rem;">🎯 Expected Output</h4>
        """, unsafe_allow_html=True)
        expected_output = st.number_input(
            "Expected Coal Output (Tonnes)",
            min_value=0.0,
            value=float(st.session_state.areas_data[selected_area]['expected'].get(selected_month, 0)),
            key=f"expected_{selected_area}_{selected_month}",
            step=100.0
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card fade-in">
            <h4 style="color: var(--neon-orange); margin-bottom: 1rem;">📈 Actual Output</h4>
        """, unsafe_allow_html=True)
        actual_output = st.number_input(
            "Actual Coal Output (Tonnes)",
            min_value=0.0,
            value=float(st.session_state.areas_data[selected_area]['actual'].get(selected_month, 0)),
            key=f"actual_{selected_area}_{selected_month}",
            step=100.0
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card slide-in-right">
            <h4 style="color: var(--neon-purple); margin-bottom: 1rem;">📊 Performance</h4>
        """, unsafe_allow_html=True)
        if expected_output > 0:
            performance = (actual_output / expected_output) * 100
            if performance >= 95:
                st.markdown(f'<div style="color: var(--neon-green); font-size: 1.5rem; font-weight: bold;">✅ {performance:.1f}%</div>', unsafe_allow_html=True)
            elif performance >= 80:
                st.markdown(f'<div style="color: var(--neon-orange); font-size: 1.5rem; font-weight: bold;">⚠️ {performance:.1f}%</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="color: #ff4757; font-size: 1.5rem; font-weight: bold;">❌ {performance:.1f}%</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color: #cccccc; font-size: 1.5rem;">---</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Issue tracking
    st.markdown("""
    <div class="glass-card fade-in">
        <h3 style="color: var(--neon-blue); margin-bottom: 1.5rem; font-family: 'Orbitron', monospace;">
            🚨 Issue Tracking
        </h3>
        <p style="color: #cccccc; margin-bottom: 1rem; font-size: 0.9rem;">
            Select issues that affected production this month
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        land_issues = st.checkbox(
            "🏗️ Land Acquisition Issues", 
            value=st.session_state.areas_data[selected_area]['issues'].get(selected_month, {}).get('land', False),
            key=f"land_{selected_area}_{selected_month}"
        )
    
    with col2:
        climate_issues = st.checkbox(
            "🌪️ Climate Calamities",
            value=st.session_state.areas_data[selected_area]['issues'].get(selected_month, {}).get('climate', False),
            key=f"climate_{selected_area}_{selected_month}"
        )
    
    # Custom issue input (only show if actual < expected)
    if expected_output > 0 and actual_output < expected_output:
        st.markdown("""
        <div style="background: rgba(245, 158, 11, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid var(--neon-orange); margin: 1rem 0;">
            <h4 style="color: var(--neon-orange); margin-bottom: 0.5rem;">⚠️ Production Shortfall Detected</h4>
            <p style="color: #cccccc; margin: 0; font-size: 0.9rem;">
                Actual production is below expected. Please specify other issues affecting production.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        custom_issue = st.text_area(
            "Other Issues (Optional)",
            value=st.session_state.areas_data[selected_area]['issues'].get(selected_month, {}).get('custom', ''),
            placeholder="Describe any other issues affecting production (e.g., equipment breakdown, labor shortage, regulatory issues, etc.)",
            key=f"custom_{selected_area}_{selected_month}",
            height=100
        )
    else:
        custom_issue = st.session_state.areas_data[selected_area]['issues'].get(selected_month, {}).get('custom', '')
    
    # Save button
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;">
    """, unsafe_allow_html=True)
    
    if st.button("💾 Save Data", key=f"save_{selected_area}_{selected_month}", type="primary"):
        with st.spinner("Saving data..."):
            st.session_state.areas_data[selected_area]['expected'][selected_month] = expected_output
            st.session_state.areas_data[selected_area]['actual'][selected_month] = actual_output
            st.session_state.areas_data[selected_area]['issues'][selected_month] = {
                'land': land_issues,
                'climate': climate_issues,
                'custom': custom_issue
            }
            st.success("✅ Data saved successfully!")
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def create_individual_analytics():
    """Create individual area analytics"""
    create_header_with_logo()
    
    st.markdown("""
    <div class="glass-card fade-in">
        <h2 style="color: var(--neon-blue); margin-bottom: 1.5rem; font-family: 'Orbitron', monospace;">
            📈 Individual Area Analytics
        </h2>
        <p style="color: #cccccc; margin-bottom: 2rem;">
            Analyze production performance for individual mining areas with detailed insights.
        </p>
    """, unsafe_allow_html=True)
    
    # Area selector
    st.markdown("""
    <div class="glass-card slide-in-left">
        <h3 style="color: var(--neon-green); margin-bottom: 1rem;">📍 Select Area for Analysis</h3>
    """, unsafe_allow_html=True)
    selected_area = st.selectbox("Select Area for Analysis", list(st.session_state.areas_data.keys()), key="analytics_area")
    st.markdown("</div>", unsafe_allow_html=True)
    
    area_data = st.session_state.areas_data[selected_area]
    
    # Prepare data for plotting
    months = st.session_state.months
    expected_data = [area_data['expected'].get(month, 0) for month in months]
    actual_data = [area_data['actual'].get(month, 0) for month in months]
    
    # Create enhanced 3D-style chart
    fig = go.Figure()
    
    # Expected production line (green with glow effect)
    fig.add_trace(go.Scatter(
        x=months,
        y=expected_data,
        mode='lines+markers',
        name='Expected Output',
        line=dict(color='#10b981', width=4),
        marker=dict(size=12, color='#10b981', line=dict(width=2, color='#ffffff')),
        hovertemplate='<b>%{x}</b><br>Expected: %{y:,.0f} T<extra></extra>'
    ))
    
    # Actual production line (red with glow effect)
    fig.add_trace(go.Scatter(
        x=months,
        y=actual_data,
        mode='lines+markers',
        name='Actual Output',
        line=dict(color='#ef4444', width=4),
        marker=dict(size=12, color='#ef4444', line=dict(width=2, color='#ffffff')),
        hovertemplate='<b>%{x}</b><br>Actual: %{y:,.0f} T<extra></extra>'
    ))
    
    # Add issue indicators with enhanced styling
    for i, month in enumerate(months):
        issues = area_data['issues'].get(month, {})
        if issues.get('land', False):
            fig.add_vrect(
                x0=i-0.4, x1=i+0.4,
                fillcolor='rgba(16, 185, 129, 0.3)',
                layer="below",
                line_width=0,
                annotation_text="Land Issues",
                annotation_position="top"
            )
        if issues.get('climate', False):
            fig.add_vrect(
                x0=i-0.2, x1=i+0.2,
                fillcolor='rgba(245, 158, 11, 0.3)',
                layer="below",
                line_width=0,
                annotation_text="Climate Issues",
                annotation_position="top"
            )
        if issues.get('custom', ''):
            fig.add_vrect(
                x0=i-0.1, x1=i+0.1,
                fillcolor='rgba(139, 92, 246, 0.3)',
                layer="below",
                line_width=0,
                annotation_text="Other Issues",
                annotation_position="top"
            )
    
    # Enhanced layout with futuristic styling
    fig.update_layout(
        title=dict(
            text=f'<b>{selected_area}</b> - Production Analysis',
            font=dict(size=24, color='#ffffff', family='Orbitron'),
            x=0.5
        ),
        xaxis=dict(
            title='Month',
            titlefont=dict(size=16, color='#00d4ff'),
            tickfont=dict(size=14, color='#ffffff'),
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.2)'
        ),
        yaxis=dict(
            title='Coal Output (Tonnes)',
            titlefont=dict(size=16, color='#00d4ff'),
            tickfont=dict(size=14, color='#ffffff'),
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.2)'
        ),
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 0, 0, 0.1)',
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=14, color='#ffffff')
        )
    )
    
    st.markdown("""
    <div class="glass-card fade-in">
        <h3 style="color: var(--neon-blue); margin-bottom: 1.5rem; font-family: 'Orbitron', monospace;">
            📊 Production Trend Analysis
        </h3>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced Performance metrics
    st.markdown("""
    <div class="glass-card fade-in">
        <h3 style="color: var(--neon-blue); margin-bottom: 1.5rem; font-family: 'Orbitron', monospace;">
            📈 Performance Metrics
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_expected = sum(expected_data)
    total_actual = sum(actual_data)
    avg_performance = (total_actual / total_expected * 100) if total_expected > 0 else 0
    
    with col1:
        st.markdown(f"""
        <div class="metric-card slide-in-left pulse">
            <h4 style="color: var(--neon-green); margin-bottom: 0.5rem;">🎯 Total Expected</h4>
            <div style="font-size: 2rem; font-weight: bold; color: var(--neon-green);">{total_expected:,.0f} T</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card fade-in pulse">
            <h4 style="color: var(--neon-orange); margin-bottom: 0.5rem;">📈 Total Actual</h4>
            <div style="font-size: 2rem; font-weight: bold; color: var(--neon-orange);">{total_actual:,.0f} T</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        performance_color = "#10b981" if avg_performance >= 95 else "#f59e0b" if avg_performance >= 80 else "#ef4444"
        st.markdown(f"""
        <div class="metric-card slide-in-right pulse">
            <h4 style="color: {performance_color}; margin-bottom: 0.5rem;">📊 Avg Performance</h4>
            <div style="font-size: 2rem; font-weight: bold; color: {performance_color};">{avg_performance:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        variance = total_actual - total_expected
        variance_color = "#10b981" if variance >= 0 else "#ef4444"
        st.markdown(f"""
        <div class="metric-card fade-in pulse">
            <h4 style="color: {variance_color}; margin-bottom: 0.5rem;">📉 Variance</h4>
            <div style="font-size: 2rem; font-weight: bold; color: {variance_color};">{variance:,.0f} T</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def create_overall_dashboard():
    """Create overall production dashboard"""
    create_header_with_logo()
    st.markdown("### 🏭 Combined Production Analytics")
    
    # Calculate overall data
    months = st.session_state.months
    total_expected = []
    total_actual = []
    
    for month in months:
        month_expected = sum(st.session_state.areas_data[area]['expected'].get(month, 0) 
                           for area in st.session_state.areas_data)
        month_actual = sum(st.session_state.areas_data[area]['actual'].get(month, 0) 
                          for area in st.session_state.areas_data)
        total_expected.append(month_expected)
        total_actual.append(month_actual)
    
    # Create overall chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=total_expected,
        mode='lines+markers',
        name='Total Expected Output',
        line=dict(color='#4caf50', width=4),
        marker=dict(size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=total_actual,
        mode='lines+markers',
        name='Total Actual Output',
        line=dict(color='#f44336', width=4),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        title='Overall Production Analysis - All Areas Combined',
        xaxis_title='Month',
        yaxis_title='Coal Output (Tonnes)',
        template='plotly_dark',
        height=600,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Overall metrics
    col1, col2, col3, col4 = st.columns(4)
    
    grand_total_expected = sum(total_expected)
    grand_total_actual = sum(total_actual)
    overall_performance = (grand_total_actual / grand_total_expected * 100) if grand_total_expected > 0 else 0
    
    with col1:
        st.metric("Grand Total Expected", f"{grand_total_expected:,.0f} T")
    with col2:
        st.metric("Grand Total Actual", f"{grand_total_actual:,.0f} T")
    with col3:
        st.metric("Overall Performance", f"{overall_performance:.1f}%")
    with col4:
        grand_variance = grand_total_actual - grand_total_expected
        st.metric("Grand Variance", f"{grand_variance:,.0f} T")
    
    # Area-wise summary table
    st.markdown("#### Area-wise Summary")
    summary_data = []
    for area in st.session_state.areas_data:
        area_expected = sum(st.session_state.areas_data[area]['expected'].values())
        area_actual = sum(st.session_state.areas_data[area]['actual'].values())
        area_performance = (area_actual / area_expected * 100) if area_expected > 0 else 0
        
        # Count issues
        land_issues = sum(1 for issues in st.session_state.areas_data[area]['issues'].values() if issues.get('land', False))
        climate_issues = sum(1 for issues in st.session_state.areas_data[area]['issues'].values() if issues.get('climate', False))
        custom_issues = sum(1 for issues in st.session_state.areas_data[area]['issues'].values() if issues.get('custom', ''))
        
        summary_data.append({
            'Area': area,
            'Expected (T)': f"{area_expected:,.0f}",
            'Actual (T)': f"{area_actual:,.0f}",
            'Performance (%)': f"{area_performance:.1f}",
            'Land Issues': land_issues,
            'Climate Issues': climate_issues,
            'Other Issues': custom_issues
        })
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True)

def create_sidebar():
    """Create sidebar navigation"""
    # Enhanced sidebar with futuristic styling
    logo_base64 = get_image_base64()
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 1rem 0;">
        <img src="data:image/jpeg;base64,{logo_base64}" style="height:80px; width:auto; filter: drop-shadow(0 0 10px var(--neon-blue));" />
        <h3 style="color: var(--neon-blue); margin-top: 1rem; font-family: 'Orbitron', monospace;">BCCL Analytics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # System status
    if st.session_state.get('setup_complete', False):
        st.sidebar.markdown("""
        <div style="background: rgba(16, 185, 129, 0.2); padding: 1rem; border-radius: 10px; border-left: 4px solid var(--neon-green); margin: 1rem 0;">
            <h4 style="color: var(--neon-green); margin: 0;">✅ System Active</h4>
            <p style="color: #cccccc; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                Areas: {num_areas} | Duration: {duration} months
            </p>
        </div>
        """.format(
            num_areas=st.session_state.get('num_areas', 0),
            duration=st.session_state.get('time_duration', 0)
        ), unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div style="background: rgba(245, 158, 11, 0.2); padding: 1rem; border-radius: 10px; border-left: 4px solid var(--neon-orange); margin: 1rem 0;">
            <h4 style="color: var(--neon-orange); margin: 0;">⚠️ Setup Required</h4>
            <p style="color: #cccccc; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                Complete initial setup to begin
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Quick stats
    if st.session_state.get('setup_complete', False):
        total_expected = sum(
            sum(area_data['expected'].values()) 
            for area_data in st.session_state.areas_data.values()
        )
        total_actual = sum(
            sum(area_data['actual'].values()) 
            for area_data in st.session_state.areas_data.values()
        )
        
        st.sidebar.markdown("""
        <div style="background: rgba(0, 0, 0, 0.3); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <h4 style="color: var(--neon-blue); margin: 0 0 1rem 0;">📊 Quick Stats</h4>
            <div style="color: var(--neon-green); font-size: 1.2rem; font-weight: bold;">Expected: {expected:,.0f} T</div>
            <div style="color: var(--neon-orange); font-size: 1.2rem; font-weight: bold;">Actual: {actual:,.0f} T</div>
        </div>
        """.format(expected=total_expected, actual=total_actual), unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Reset button
    if st.sidebar.button("🔄 Reset Session", type="secondary"):
        for key in ['areas_data', 'num_areas', 'time_duration', 'setup_complete', 'months']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    return None  # Navigation is now in header

def main():
    """Main application function"""
    # Enable PWA before rendering pages so the manifest/sw is available
    enable_pwa()
    create_sidebar()
    
    # Initialize current page in session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'setup'
    
    # Navigation buttons using session state
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🚀 Setup", key="nav_setup", use_container_width=True):
            st.session_state.current_page = 'setup'
            st.rerun()
    
    with col2:
        if st.button("📊 Data Entry", key="nav_data", use_container_width=True):
            st.session_state.current_page = 'data'
            st.rerun()
    
    with col3:
        if st.button("📈 Analytics", key="nav_analytics", use_container_width=True):
            st.session_state.current_page = 'analytics'
            st.rerun()
    
    with col4:
        if st.button("🏭 Dashboard", key="nav_dashboard", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    # Check if setup is complete for non-setup pages
    if not st.session_state.setup_complete and st.session_state.current_page != 'setup':
        st.markdown("""
        <div class="glass-card fade-in" style="text-align: center; padding: 2rem;">
            <h2 style="color: var(--neon-orange); margin-bottom: 1rem;">⚠️ Setup Required</h2>
            <p style="color: #cccccc; margin-bottom: 2rem;">
                Please complete the initial system setup before accessing other features.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Go to Setup", key="goto_setup"):
            st.session_state.current_page = 'setup'
            st.rerun()
        return
    
    # Route to appropriate page
    if st.session_state.current_page == 'setup':
        create_setup_form()
    elif st.session_state.current_page == 'data':
        create_area_data_entry()
    elif st.session_state.current_page == 'analytics':
        create_individual_analytics()
    elif st.session_state.current_page == 'dashboard':
        create_overall_dashboard()
    else:
        # Default to setup
        create_setup_form()

if __name__ == "__main__":
    main()
