"""
APL Logistics — Profitability & Supply Chain Dashboard
========================================================
An interactive Streamlit decision-support dashboard for Customer, Product,
and Profitability Performance Analysis in Supply Chain Operations.

Data source : data/raw/APL_Logistics.csv
Author      : APL Logistics Analytics Project
"""

import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------------
# 0. PAGE CONFIGURATION
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="APL Logistics — Profitability & Supply Chain Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# 1. GLOBAL STYLE (premium light BI look)
# ----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Inter:wght@400;500;600;700&display=swap');

:root{
    --bg-page:#0A0A0D;
    --card:#17171C;
    --card-alt:#1C1C22;
    --border:rgba(255,255,255,0.08);
    --border-strong:rgba(255,255,255,0.18);
    --text:#F2F2F5;
    --text-muted:#96969F;
    --text-faint:#68686F;
    --accent:#F2703C;
    --accent-soft:rgba(242,112,60,0.14);
    --green:#3ED993;
    --red:#F2545B;
    --amber:#FFB020;
}

html, body, [class*="css"]{ font-family:'Inter', 'Segoe UI', sans-serif; }

.stApp{
    background:
        radial-gradient(circle at 88% 0%, rgba(242,112,60,0.10), transparent 42%),
        radial-gradient(circle at 6% 92%, rgba(242,112,60,0.05), transparent 45%),
        linear-gradient(180deg, #08080B 0%, #101014 100%);
}

/* Reduce the large default top gap so the hero sits closer to the top */
div[data-testid="stAppViewContainer"] .block-container{
    padding-top:1.6rem;
}

#MainMenu, footer {visibility:hidden;}
header[data-testid="stHeader"]{ background:transparent; }

/* Base text readability on the dark app background — cards, insight
   boxes and the hero keep their own explicit colors (higher specificity),
   this only covers plain/default text sitting directly on the page bg. */
div[data-testid="stAppViewContainer"] > .main p,
div[data-testid="stAppViewContainer"] > .main span,
div[data-testid="stAppViewContainer"] > .main label,
div[data-testid="stAppViewContainer"] > .main .stMarkdown,
div[data-testid="stAppViewContainer"] > .main [data-testid="stCaptionContainer"],
div[data-testid="stAppViewContainer"] > .main [data-testid="stWidgetLabel"] p{
    color:var(--text);
}
div[data-testid="stAppViewContainer"] > .main [data-testid="stCaptionContainer"]{
    color:var(--text-muted) !important;
}

section[data-testid="stSidebar"]{
    background:#0C0C10;
    margin-right: 14px;
    border-right: 1px solid var(--border);
    box-shadow: 6px 0 18px rgba(0, 0, 0, 0.35);
    border-radius:0 16px 16px 0;
}
section[data-testid="stSidebar"] * { color:#EDEDF1 !important; }
section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div{ color:#EDEDF1;}

/* Hero */
.hero{
    position:relative;
    background:linear-gradient(160deg, #121216 0%, #17171C 60%, #1B1B20 100%);
    padding:34px 40px;
    border-radius:20px;
    color:var(--text);
    margin-bottom:22px;
    box-shadow:0 10px 30px rgba(0,0,0,0.45);
    border:1px solid var(--border);
    overflow:hidden;
}
.hero-badge{
    display:inline-block;
    background:var(--accent-soft);
    border:1px solid rgba(242,112,60,0.4);
    color:#FFB78F;
    font-size:12px;
    font-weight:600;
    padding:5px 14px;
    border-radius:20px;
    margin-bottom:14px;
    position:relative;
}
.hero h1{
    font-family:'Space Grotesk', 'Inter', sans-serif;
    font-size:32px;
    font-weight:700;
    margin:0 0 4px 0;
    letter-spacing:.2px;
    color:var(--text);
    position:relative;
}
.hero h2{
    font-size:18px;
    font-weight:500;
    margin:0 0 10px 0;
    color:#C7C7D1;
    position:relative;
}
.hero p{
    font-size:14.5px;
    color:#A7A7B2;
    max-width:800px;
    margin:0;
    position:relative;
}

/* Section headers */
.section-title{
    font-size:20px;
    font-weight:700;
    color:var(--text);
    margin:8px 0 2px 0;
    display:flex;
    align-items:center;
    gap:10px;
}
.section-num{
    background:var(--accent);
    color:#1A0F08;
    font-size:12px;
    font-weight:700;
    border-radius:6px;
    padding:3px 9px;
}
.section-sub{
    color:var(--text-muted);
    font-size:13px;
    margin-bottom:14px;
}

/* KPI cards */
.kpi-card{
    background:var(--card);
    border:1px solid var(--border);
    border-radius:16px;
    padding:18px 20px;
    box-shadow:0 4px 14px rgba(0,0,0,0.3);
    height:100%;
    transition:border-color .15s ease, transform .15s ease;
}
.kpi-card:hover{
    border-color:var(--border-strong);
    transform:translateY(-2px);
}
.kpi-label{
    font-size:12.5px;
    color:var(--text-muted);
    font-weight:600;
    margin-bottom:6px;
}
.kpi-value{
    font-size:27px;
    font-weight:700;
    color:var(--text);
    line-height:1.1;
}
.kpi-sub{
    font-size:12px;
    margin-top:6px;
    font-weight:600;
}
.kpi-sub.pos{ color:var(--green); }
.kpi-sub.neg{ color:var(--red); }
.kpi-sub.neutral{ color:var(--text-muted); }

/* Insight callout */
.insight-box{
    background:var(--accent-soft);
    border-left:4px solid var(--accent);
    border-radius:12px;
    padding:14px 18px;
    margin:10px 0 20px 0;
    font-size:13.8px;
    color:#F0DCCF;
    line-height:1.55;
}
.insight-box b{ color:#FFD3B0; }

.active-view-box{
    background:rgba(255,255,255,0.03);
    border:1px solid var(--border);
    border-left:3px solid var(--accent);
    border-radius:12px;
    padding:11px 16px;
    margin:6px 0 20px 0;
}

.active-view-label{
    color:var(--text-faint);
    font-size:10.5px;
    font-weight:700;
    letter-spacing:1.2px;
    margin-bottom:4px;
}

.active-view-content{
    color:var(--text);
    font-size:13px;
    line-height:1.5;
}

.active-view-records{
    color:var(--text-muted);
    font-size:12px;
    font-weight:600;
    margin-left:10px;
    white-space:nowrap;
}

.warn-box{
    background:rgba(242,84,91,0.10);
    border-left:4px solid var(--red);
    border-radius:12px;
    padding:14px 18px;
    margin:10px 0 20px 0;
    font-size:13.8px;
    color:#FFC9CC;
    line-height:1.55;
}

.note-box{
    background:rgba(255,176,32,0.10);
    border-left:4px solid var(--amber);
    border-radius:12px;
    padding:11px 16px;
    margin:8px 0 18px 0;
    font-size:12.6px;
    color:#FFDFA6;
    line-height:1.5;
}

.chart-card{
    background:var(--card);
    border:1px solid var(--border);
    border-radius:16px;
    padding:14px 16px 4px 16px;
    box-shadow:0 4px 14px rgba(0,0,0,0.3);
    margin-bottom:18px;
}
.chart-card h4{
    color:var(--text);
    font-size:14.5px;
    font-weight:700;
    margin:2px 0 2px 4px;
}
.chart-card .chart-desc{
    color:var(--text-muted);
    font-size:12px;
    margin:0 0 6px 4px;
}

hr.divider{
    border:none;
    border-top:1px solid var(--border);
    margin:26px 0 18px 0;
}

.footer-box{
    text-align:center;
    padding:26px 10px 14px 10px;
    color:var(--text-faint);
    font-size:12.3px;
    line-height:1.6;
}
.footer-box b{ color:var(--text); }

div[data-testid="stDataFrame"]{
    border:1px solid var(--border);
    border-radius:12px;
    overflow:hidden;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

PLOTLY_TEMPLATE = "plotly_dark"
NAVY = "#F2F2F5"
BLUE = "#F2703C"
BLUE_SOFT = "#8892A6"
GREEN = "#3ED993"
RED = "#F2545B"
AMBER = "#FFB020"
PURPLE = "#9B8CFF"
CATEGORICAL_PALETTE = [BLUE, BLUE_SOFT, GREEN, AMBER, PURPLE, RED, "#3DBFC8", "#C9CED9"]


def style_fig(fig, height=380, legend=True):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=height,
        margin=dict(l=10, r=10, t=30, b=10),
        font=dict(color=NAVY, size=12.5, family="Inter, Segoe UI, sans-serif"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.08)", zeroline=False)
    return fig


# ----------------------------------------------------------------------------
# 2. DATA LOADING
# ----------------------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "APL_Logistics.csv")


@st.cache_data(show_spinner="Loading APL Logistics dataset...")
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="latin1")

    # Discount bands consistent with the analysis notebook.
    # No orders exist above 25% discount rate in this dataset.
    df["Discount_Band"] = pd.cut(
        df["Order Item Discount Rate"],
        bins=[-0.001, 0, 0.05, 0.10, 0.15, 0.20, 0.25, 1],
        labels=["No Discount", "0-5%", "5-10%", "10-15%", "15-20%", "20-25%", "Above 25%"],
        include_lowest=True,
    )
    df["Is_Loss"] = df["Order Profit Per Order"] < 0
    return df


if not os.path.exists(DATA_PATH):
    st.error(
        f"Dataset not found at `{DATA_PATH}`. "
        "Make sure `APL_Logistics.csv` is placed under `data/raw/`."
    )
    st.stop()

df = load_data(DATA_PATH)

# Discount bands actually present in the data (drop "Above 25%" — no observations)
DISCOUNT_BAND_ORDER = ["No Discount", "0-5%", "5-10%", "10-15%", "15-20%", "20-25%"]


# ----------------------------------------------------------------------------
# 3. FORMATTING HELPERS
# ----------------------------------------------------------------------------
def fmt_money(x, compact=True):
    if pd.isna(x):
        return "-"
    sign = "-" if x < 0 else ""
    x = abs(x)
    if compact:
        if x >= 1_000_000:
            return f"{sign}{x/1_000_000:.2f}M"
        if x >= 1_000:
            return f"{sign}{x/1_000:.1f}K"
    return f"{sign}{x:,.2f}"


def fmt_money_full(x):
    if pd.isna(x):
        return "-"
    return f"{x:,.2f}"


def fmt_pct(x, dp=2):
    if pd.isna(x):
        return "-"
    return f"{x:.{dp}f}%"


def fmt_int(x):
    if pd.isna(x):
        return "-"
    return f"{int(x):,}"


def kpi_card(label, value, sub=None, sub_type="neutral"):
    sub_html = f'<div class="kpi-sub {sub_type}">{sub}</div>' if sub else ""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(number, title, subtitle):
    st.markdown(
        f"""
        <div class="section-title"><span class="section-num">{number}</span> {title}</div>
        <div class="section-sub">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def insight(text):
    st.markdown(f'<div class="insight-box">💡 <b>Executive Insight —</b> {text}</div>', unsafe_allow_html=True)


def warn_insight(text):
    st.markdown(f'<div class="warn-box">⚠️ <b>Risk Flag —</b> {text}</div>', unsafe_allow_html=True)


def note(text):
    st.markdown(f'<div class="note-box">ℹ️ {text}</div>', unsafe_allow_html=True)


def chart_card_open(title, desc=""):
    desc_html = f'<div class="chart-desc">{desc}</div>' if desc else ""
    st.markdown(f'<div class="chart-card"><h4>{title}</h4>{desc_html}', unsafe_allow_html=True)


def chart_card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def clean_table(dframe, rename_map=None, pct_cols=None, money_cols=None, int_cols=None, height=None):
    """Return a display-ready copy of a table: renamed, rounded, formatted."""
    t = dframe.copy()
    if rename_map:
        t = t.rename(columns=rename_map)
    pct_cols = pct_cols or []
    money_cols = money_cols or []
    int_cols = int_cols or []
    for c in pct_cols:
        if c in t.columns:
            t[c] = t[c].round(2)
    for c in money_cols:
        if c in t.columns:
            t[c] = t[c].round(2)
    for c in int_cols:
        if c in t.columns:
            t[c] = t[c].astype(int)
    if height is not None:
        st.dataframe(t, hide_index=True, use_container_width=True, height=height)
    else:
        st.dataframe(t, hide_index=True, use_container_width=True)


# ----------------------------------------------------------------------------
# 4. HERO HEADER
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <span class="hero-badge">PROFITABILITY INTELLIGENCE</span>
        <h1>APL Logistics</h1>
        <h2>Profitability &amp; Supply Chain Intelligence Dashboard</h2>
        <p>Customer, product, discount and geographic profitability intelligence for
        decision-ready analysis. Explore where the business is truly creating — or losing —
        value across customers, products, categories, discounts, markets and regions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# 5. GLOBAL FILTERS (SIDEBAR)
# ----------------------------------------------------------------------------
st.sidebar.markdown("### 🔎 Global Filters")
st.sidebar.caption("Filters apply to every module below.")

# ---------- DEFAULT FILTER VALUES ----------
if "sel_segment" not in st.session_state:
    st.session_state.sel_segment = "All"

if "sel_category" not in st.session_state:
    st.session_state.sel_category = "All"

if "sel_product" not in st.session_state:
    st.session_state.sel_product = "All"

if "sel_market" not in st.session_state:
    st.session_state.sel_market = "All"

if "sel_region" not in st.session_state:
    st.session_state.sel_region = "All"

if "discount_range" not in st.session_state:
    st.session_state.discount_range = (0, 25)

# ---------- FILTER OPTIONS ----------
segment_options = ["All"] + sorted(
    df["Customer Segment"].dropna().unique().tolist()
)

category_options = ["All"] + sorted(
    df["Category Name"].dropna().unique().tolist()
)

market_options = ["All"] + sorted(
    df["Market"].dropna().unique().tolist()
)

region_options = ["All"] + sorted(
    df["Order Region"].dropna().unique().tolist()
)

# ---------- CUSTOMER SEGMENT ----------
sel_segment = st.sidebar.selectbox(
    "Customer Segment",
    segment_options,
    key="sel_segment"
)

# ---------- CATEGORY ----------
sel_category = st.sidebar.selectbox(
    "Category",
    category_options,
    key="sel_category"
)

# ---------- PRODUCT ----------
if sel_category == "All":
    product_pool = df
else:
    product_pool = df[df["Category Name"] == sel_category]

product_options = ["All"] + sorted(
    product_pool["Product Name"].dropna().unique().tolist()
)

# If current product is no longer valid after changing category,
# automatically return it to All.
if st.session_state.sel_product not in product_options:
    st.session_state.sel_product = "All"

sel_product = st.sidebar.selectbox(
    "Product",
    product_options,
    key="sel_product"
)

# ---------- MARKET ----------
sel_market = st.sidebar.selectbox(
    "Market",
    market_options,
    key="sel_market"
)

# ---------- REGION ----------
sel_region = st.sidebar.selectbox(
    "Order Region",
    region_options,
    key="sel_region"
)

# ---------- DISCOUNT ----------
discount_range = st.sidebar.slider(
    "Discount Rate (Order Item Discount Rate)",
    min_value=0,
    max_value=25,
    value=(0, 25),
    step=1,
    format="%d%%",
    key="discount_range"
)

discount_min, discount_max = discount_range

# ---------- RESET ----------
def reset_filters():
    st.session_state.sel_segment = "All"
    st.session_state.sel_category = "All"
    st.session_state.sel_product = "All"
    st.session_state.sel_market = "All"
    st.session_state.sel_region = "All"
    st.session_state.discount_range = (0, 25)

st.sidebar.markdown("---")

st.sidebar.button(
    "↺ Reset filters",
    on_click=reset_filters
)

st.sidebar.markdown(
    """
    <div style="font-size:11.5px; color:#6E6E77; margin-top:6px;">
    Dashboard analytical tiers and risk scores are model-defined indicators,
    not official APL Logistics KPIs.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---- apply filters -> df_filtered ----
df_filtered = df.copy()
if sel_segment != "All":
    df_filtered = df_filtered[df_filtered["Customer Segment"] == sel_segment]
if sel_category != "All":
    df_filtered = df_filtered[df_filtered["Category Name"] == sel_category]
if sel_product != "All":
    df_filtered = df_filtered[df_filtered["Product Name"] == sel_product]
if sel_market != "All":
    df_filtered = df_filtered[df_filtered["Market"] == sel_market]
if sel_region != "All":
    df_filtered = df_filtered[df_filtered["Order Region"] == sel_region]
df_filtered = df_filtered[
    (df_filtered["Order Item Discount Rate"] * 100 >= discount_min)
    & (df_filtered["Order Item Discount Rate"] * 100 <= discount_max)
]

if df_filtered.empty:
    st.warning("No records match the current filter combination. Please broaden your filters.")
    st.stop()

active_filters = []
if sel_segment != "All":
    active_filters.append(f"Segment: {sel_segment}")
if sel_category != "All":
    active_filters.append(f"Category: {sel_category}")
if sel_product != "All":
    active_filters.append(f"Product: {sel_product}")
if sel_market != "All":
    active_filters.append(f"Market: {sel_market}")
if sel_region != "All":
    active_filters.append(f"Region: {sel_region}")
if (discount_min, discount_max) != (0, 25):
    active_filters.append(f"Discount: {discount_min}-{discount_max}%")
filter_caption = " • ".join(active_filters) if active_filters else "No filters applied — showing full dataset"

st.markdown(
    f"""
    <div class="active-view-box">
        <div class="active-view-label">CURRENT ANALYSIS VIEW</div>
        <div class="active-view-content">
            {filter_caption}
            <span class="active-view-records">
                Records: {len(df_filtered):,} of {len(df):,}
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# CORE FIGURES USED ACROSS MODULES
# ============================================================================
total_sales = df_filtered["Sales"].sum()
total_profit = df_filtered["Order Profit Per Order"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0
profitability_status = "Profitable" if total_profit >= 0 else "Loss-Making"

# ============================================================================
# TOP-LEVEL EXECUTIVE INSIGHT
# ============================================================================
insight(
    f"The current filtered view generates <b>{fmt_money(total_sales)}</b> in revenue at a "
    f"<b>{fmt_pct(profit_margin)}</b> profit margin, resulting in <b>{fmt_money(total_profit)}</b> "
    f"total profit. Revenue scale alone does not capture business value — use the modules below "
    f"to identify the customer, product, discount, market and regional drivers behind this result."
)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ============================================================================
# MODULE 01 — REVENUE & PROFIT OVERVIEW
# ============================================================================
section_header("01", "Revenue &amp; Profit Overview", "What is the overall financial position of the business?")

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Total Sales", fmt_money(total_sales), fmt_money_full(total_sales) + " total", "neutral")
with c2:
    kpi_card(
        "Total Profit",
        fmt_money(total_profit),
        fmt_money_full(total_profit) + " total",
        "pos" if total_profit >= 0 else "neg",
    )
with c3:
    kpi_card("Profit Margin", fmt_pct(profit_margin), "Profit ÷ Sales × 100", "pos" if profit_margin >= 0 else "neg")
with c4:
    kpi_card(
        "Profitability Status",
        profitability_status,
        "Based on current filtered view",
        "pos" if profitability_status == "Profitable" else "neg",
    )

st.write("")

col_a, col_b = st.columns(2)

with col_a:
    chart_card_open(
        "Revenue vs Profit by Market",
        "High revenue does not automatically mean high profit — compare scale against actual profit generated.",
    )
    mkt_rev_profit = (
        df_filtered.groupby("Market", observed=True)
        .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Order Profit Per Order", "sum"))
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )
    fig_rp = go.Figure()
    fig_rp.add_bar(x=mkt_rev_profit["Market"], y=mkt_rev_profit["Total_Sales"], name="Revenue", marker_color=BLUE_SOFT)
    fig_rp.add_bar(x=mkt_rev_profit["Market"], y=mkt_rev_profit["Total_Profit"], name="Profit", marker_color=GREEN)
    fig_rp.update_layout(barmode="group", yaxis_title="Amount")
    st.plotly_chart(style_fig(fig_rp), use_container_width=True, key="chart_1")
    chart_card_close()

with col_b:
    chart_card_open(
        "Profit Margin by Discount Band",
        "No usable order-date field exists, so profitability is compared across discount depth instead of time.",
    )
    band_summary = (
        df_filtered.groupby("Discount_Band", observed=False)
        .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Order Profit Per Order", "sum"))
        .reindex(DISCOUNT_BAND_ORDER)
        .reset_index()
    )
    band_summary["Profit_Margin_%"] = np.where(
        band_summary["Total_Sales"] > 0, band_summary["Total_Profit"] / band_summary["Total_Sales"] * 100, np.nan
    )
    fig_band = px.bar(
        band_summary,
        x="Discount_Band",
        y="Profit_Margin_%",
        text=band_summary["Profit_Margin_%"].round(2).astype(str) + "%",
        color_discrete_sequence=[BLUE],
    )
    fig_band.update_traces(textposition="outside")
    fig_band.update_layout(xaxis_title="Discount Band", yaxis_title="Profit Margin (%)")
    st.plotly_chart(style_fig(fig_band), use_container_width=True, key="chart_2")
    chart_card_close()

no_disc_margin = band_summary.loc[band_summary["Discount_Band"] == "No Discount", "Profit_Margin_%"].values
deep_disc_margin = band_summary.loc[band_summary["Discount_Band"] == "20-25%", "Profit_Margin_%"].values
if len(no_disc_margin) and len(deep_disc_margin) and not np.isnan(no_disc_margin[0]) and not np.isnan(deep_disc_margin[0]):
    insight(
        f"Observed profit margin declines from <b>{fmt_pct(no_disc_margin[0])}</b> with no discount to "
        f"<b>{fmt_pct(deep_disc_margin[0])}</b> at the 20-25% discount band within this view. This reflects "
        f"an observed association between discount depth and margin, not a proven causal effect."
    )

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ============================================================================
# MODULE 02 — CUSTOMER VALUE DASHBOARD
# ============================================================================
section_header("02", "Customer Value Dashboard", "Which customers create value, and which customers destroy it?")

customer_analysis = (
    df_filtered.groupby("Customer Id", observed=True)
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Order Profit Per Order", "sum"),
        Orders=("Order Profit Per Order", "size"),
    )
    .reset_index()
)
customer_analysis["Profit_Margin_%"] = np.where(
    customer_analysis["Total_Sales"] > 0,
    customer_analysis["Total_Profit"] / customer_analysis["Total_Sales"] * 100,
    np.nan,
)

total_customers = customer_analysis["Customer Id"].nunique()
customer_value_index = total_profit / total_customers if total_customers else 0
loss_making_customers = int((customer_analysis["Total_Profit"] < 0).sum())
loss_making_pct = (loss_making_customers / total_customers * 100) if total_customers else 0

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Total Customers", fmt_int(total_customers), "Unique Customer IDs", "neutral")
with c2:
    kpi_card(
        "Customer Value Index",
        fmt_money_full(customer_value_index),
        "Total Profit ÷ Number of Customers",
        "pos" if customer_value_index >= 0 else "neg",
    )
with c3:
    kpi_card(
        "Loss-Making Customers",
        fmt_int(loss_making_customers),
        f"{fmt_pct(loss_making_pct)} of filtered customers",
        "neg",
    )
with c4:
    top_cust_share = (
        customer_analysis.sort_values("Total_Profit", ascending=False).head(10)["Total_Profit"].sum()
        / total_profit
        * 100
        if total_profit
        else 0
    )
    kpi_card("Top 10 Customer Profit Share", fmt_pct(top_cust_share), "Share of total profit", "neutral")

insight(
    f"<b>{fmt_int(loss_making_customers)}</b> of <b>{fmt_int(total_customers)}</b> customers "
    f"(<b>{fmt_pct(loss_making_pct)}</b>) are loss-making within the current view. Review customer "
    f"rankings below to distinguish high-value relationships from accounts requiring attention."
)

col_a, col_b = st.columns(2)
with col_a:
    chart_card_open("Top 10 Customers by Profit", "Ranked by aggregate profit within the current filtered view.")
    top10 = customer_analysis.sort_values("Total_Profit", ascending=False).head(10).copy()
    top10["Customer Id"] = top10["Customer Id"].astype(str)
    fig_top10 = px.bar(
        top10.sort_values("Total_Profit"),
        x="Total_Profit",
        y="Customer Id",
        orientation="h",
        color_discrete_sequence=[GREEN],
        text=top10.sort_values("Total_Profit")["Total_Profit"].round(0).map(lambda v: f"{v:,.0f}"),
    )
    fig_top10.update_traces(textposition="outside")
    fig_top10.update_layout(xaxis_title="Total Profit", yaxis_title="Customer ID", yaxis_type="category")
    st.plotly_chart(style_fig(fig_top10, height=360), use_container_width=True, key="chart_3")
    chart_card_close()

with col_b:
    chart_card_open("Bottom 10 Customers by Profit", "Customers with the largest aggregate losses — require review.")
    bottom10 = customer_analysis.sort_values("Total_Profit", ascending=True).head(10).copy()
    bottom10["Customer Id"] = bottom10["Customer Id"].astype(str)
    fig_bottom10 = px.bar(
        bottom10.sort_values("Total_Profit", ascending=False),
        x="Total_Profit",
        y="Customer Id",
        orientation="h",
        color_discrete_sequence=[RED],
        text=bottom10.sort_values("Total_Profit", ascending=False)["Total_Profit"].round(0).map(lambda v: f"{v:,.0f}"),
    )
    fig_bottom10.update_traces(textposition="outside")
    fig_bottom10.update_layout(xaxis_title="Total Profit", yaxis_title="Customer ID", yaxis_type="category")
    st.plotly_chart(style_fig(fig_bottom10, height=360), use_container_width=True, key="chart_4")
    chart_card_close()

col_c, col_d = st.columns(2)

with col_c:
    chart_card_open("Customer Segment Profit Contribution", "Customer Segment is an actual dataset field.")
    seg_analysis = (
        df_filtered.groupby("Customer Segment", observed=True)
        .agg(
            Customers=("Customer Id", "nunique"),
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Order Profit Per Order", "sum"),
        )
        .reset_index()
    )
    seg_analysis["Profit_Margin_%"] = np.where(
        seg_analysis["Total_Sales"] > 0, seg_analysis["Total_Profit"] / seg_analysis["Total_Sales"] * 100, np.nan
    )
    seg_analysis["Profit_Contribution_%"] = (
        seg_analysis["Total_Profit"] / total_profit * 100 if total_profit else np.nan
    )
    fig_seg = px.bar(
        seg_analysis.sort_values("Total_Profit", ascending=False),
        x="Customer Segment",
        y="Total_Profit",
        color="Customer Segment",
        color_discrete_sequence=CATEGORICAL_PALETTE,
        text=seg_analysis.sort_values("Total_Profit", ascending=False)["Total_Profit"].round(0).map(lambda v: f"{v:,.0f}"),
    )
    fig_seg.update_traces(textposition="outside")
    fig_seg.update_layout(yaxis_title="Total Profit", xaxis_title="")
    st.plotly_chart(style_fig(fig_seg, height=340, legend=False), use_container_width=True, key="chart_5")
    chart_card_close()

with col_d:
    chart_card_open(
        "Profit Contribution by Customer Value Tier",
        "Model-defined quartile tiers based on total customer profit — analytical, not official segments.",
    )
    cvt = customer_analysis.copy()
    if cvt["Customer Id"].nunique() >= 4:
        cvt["Customer_Value_Tier"] = pd.qcut(
            cvt["Total_Profit"].rank(method="first"),
            q=4,
            labels=["Low Value", "Medium-Low Value", "Medium-High Value", "High Value"],
        )
        tier_summary = (
            cvt.groupby("Customer_Value_Tier", observed=True)
            .agg(Customers=("Customer Id", "count"), Total_Profit=("Total_Profit", "sum"))
            .reindex(["Low Value", "Medium-Low Value", "Medium-High Value", "High Value"])
            .reset_index()
        )
        tier_summary["Profit_Contribution_%"] = (
            tier_summary["Total_Profit"] / total_profit * 100 if total_profit else np.nan
        )
        fig_tier = px.bar(
            tier_summary,
            x="Customer_Value_Tier",
            y="Total_Profit",
            color="Customer_Value_Tier",
            color_discrete_sequence=CATEGORICAL_PALETTE,
            text=tier_summary["Total_Profit"].round(0).map(lambda v: f"{v:,.0f}"),
        )
        fig_tier.update_traces(textposition="outside")
        fig_tier.update_layout(xaxis_title="", yaxis_title="Total Profit")
        st.plotly_chart(style_fig(fig_tier, height=340, legend=False), use_container_width=True, key="chart_6")
    else:
        st.info("Not enough distinct customers in the current filtered view to compute quartile tiers.")
    chart_card_close()

note(
    "Customer Value Tiers are model-defined quartiles based on total customer profit within the "
    "current filtered view. They are analytical tiers, not official APL Logistics customer segments."
)

with st.expander("📋 View detailed customer tables (Top / Bottom / Segment / Tiers / Loss-Making)"):
    t1, t2, t3, t4 = st.tabs(["Top 10 Customers", "Bottom 10 Customers", "Segment Contribution", "Customer Value Tiers"])
    with t1:
        clean_table(
            top10.sort_values("Total_Profit", ascending=False)[["Customer Id", "Total_Sales", "Total_Profit", "Profit_Margin_%"]],
            rename_map={
                "Customer Id": "Customer ID",
                "Total_Sales": "Total Sales",
                "Total_Profit": "Total Profit",
                "Profit_Margin_%": "Profit Margin (%)",
            },
        )
    with t2:
        clean_table(
            bottom10.sort_values("Total_Profit")[["Customer Id", "Total_Sales", "Total_Profit", "Profit_Margin_%"]],
            rename_map={
                "Customer Id": "Customer ID",
                "Total_Sales": "Total Sales",
                "Total_Profit": "Total Profit",
                "Profit_Margin_%": "Profit Margin (%)",
            },
        )
    with t3:
        clean_table(
            seg_analysis[["Customer Segment", "Customers", "Total_Sales", "Total_Profit", "Profit_Margin_%", "Profit_Contribution_%"]],
            rename_map={
                "Total_Sales": "Total Sales",
                "Total_Profit": "Total Profit",
                "Profit_Margin_%": "Profit Margin (%)",
                "Profit_Contribution_%": "Profit Contribution (%)",
            },
        )
    with t4:
        if cvt["Customer Id"].nunique() >= 4:
            clean_table(
                tier_summary.rename(columns={"Customer_Value_Tier": "Customer Value Tier"})[
                    ["Customer Value Tier", "Customers", "Total_Profit", "Profit_Contribution_%"]
                ],
                rename_map={"Total_Profit": "Total Profit", "Profit_Contribution_%": "Profit Contribution (%)"},
            )
        else:
            st.info("Not enough distinct customers to display tiers for this filter selection.")

with st.expander("🔻 View 20 largest aggregate customer losses"):
    worst20 = (
        customer_analysis[customer_analysis["Total_Profit"] < 0]
        .sort_values("Total_Profit")
        .head(20)[["Customer Id", "Total_Sales", "Total_Profit", "Profit_Margin_%"]]
    )
    if worst20.empty:
        st.info("No loss-making customers in the current filtered view.")
    else:
        clean_table(
            worst20,
            rename_map={
                "Customer Id": "Customer ID",
                "Total_Sales": "Total Sales",
                "Total_Profit": "Total Profit",
                "Profit_Margin_%": "Profit Margin (%)",
            },
        )
        note(
            "These 20 loss-making customers are recommended for review of pricing structure, "
            "discount exposure, product mix, and service economics."
        )

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ============================================================================
# MODULE 03 — PRODUCT & CATEGORY PERFORMANCE
# ============================================================================
section_header("03", "Product &amp; Category Performance", "Which products and categories actually create margin?")

product_analysis = (
    df_filtered.groupby("Product Name", observed=True)
    .agg(
        Orders=("Order Profit Per Order", "size"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Order Profit Per Order", "sum"),
    )
    .reset_index()
)
product_analysis["Profit_Margin_%"] = np.where(
    product_analysis["Total_Sales"] > 0, product_analysis["Total_Profit"] / product_analysis["Total_Sales"] * 100, np.nan
)

# Use a minimum order-count threshold so single/rare orders don't dominate margin rankings.
MIN_ORDERS_PRODUCT = 5 if len(product_analysis) > 15 else 1
product_reliable = product_analysis[product_analysis["Orders"] >= MIN_ORDERS_PRODUCT].copy()
if product_reliable.empty:
    product_reliable = product_analysis.copy()

col_a, col_b = st.columns([1, 1.15])
with col_a:
    chart_card_open(
        "Top 10 Products by Profit Margin",
        f"Products with at least {MIN_ORDERS_PRODUCT} order(s) in the current view.",
    )
    top10_products = product_reliable.sort_values("Profit_Margin_%", ascending=False).head(10)
    fig_p10 = px.bar(
        top10_products.sort_values("Profit_Margin_%"),
        x="Profit_Margin_%",
        y="Product Name",
        orientation="h",
        color_discrete_sequence=[BLUE],
        text=top10_products.sort_values("Profit_Margin_%")["Profit_Margin_%"].round(2).astype(str) + "%",
    )
    fig_p10.update_traces(textposition="outside")
    fig_p10.update_layout(xaxis_title="Profit Margin (%)", yaxis_title="")
    st.plotly_chart(style_fig(fig_p10, height=380), use_container_width=True, key="chart_7")
    chart_card_close()

with col_b:
    chart_card_open(
        "Revenue Scale vs Margin Efficiency",
        "Each point is a product. The dashed line marks the overall profit margin for this view.",
    )
    fig_scatter = px.scatter(
        product_reliable,
        x="Total_Sales",
        y="Profit_Margin_%",
        size="Orders",
        color="Profit_Margin_%",
        color_continuous_scale=["#F2545B", "#FFB020", "#3DBFC8", "#3ED993"],
        hover_name="Product Name",
        labels={"Total_Sales": "Total Sales", "Profit_Margin_%": "Profit Margin (%)"},
    )
    fig_scatter.add_hline(
        y=profit_margin, line_dash="dash", line_color=NAVY,
        annotation_text=f"Overall Margin {profit_margin:.2f}%", annotation_position="top left",
    )
    st.plotly_chart(style_fig(fig_scatter, height=380), use_container_width=True, key="chart_8")
    chart_card_close()

# High-Revenue / Low-Margin Watchlist (dynamic — top revenue quartile, below overall margin)
if len(product_reliable) >= 4:
    revenue_threshold = product_reliable["Total_Sales"].quantile(0.75)
    watchlist = product_reliable[
        (product_reliable["Total_Sales"] >= revenue_threshold) & (product_reliable["Profit_Margin_%"] < profit_margin)
    ].sort_values("Profit_Margin_%")
else:
    watchlist = product_reliable[product_reliable["Profit_Margin_%"] < profit_margin].sort_values("Profit_Margin_%")

if not watchlist.empty:
    warn_insight(
        f"<b>{len(watchlist)}</b> product(s) combine high revenue scale with a profit margin below the "
        f"overall {fmt_pct(profit_margin)} — a high-revenue / low-margin watchlist worth reviewing for "
        f"pricing, discount optimization, or product-cost review."
    )

with st.expander("📋 View detailed product profitability table"):
    clean_table(
        product_analysis.sort_values("Total_Profit", ascending=False)[
            ["Product Name", "Orders", "Total_Sales", "Total_Profit", "Profit_Margin_%"]
        ],
        rename_map={"Total_Sales": "Total Sales", "Total_Profit": "Total Profit", "Profit_Margin_%": "Profit Margin (%)"},
        height=380,
    )

with st.expander("⚠️ View High-Revenue / Low-Margin watchlist"):
    if watchlist.empty:
        st.info("No products currently meet the high-revenue / below-average-margin criteria in this view.")
    else:
        clean_table(
            watchlist[["Product Name", "Orders", "Total_Sales", "Total_Profit", "Profit_Margin_%"]],
            rename_map={
                "Total_Sales": "Total Sales", "Total_Profit": "Total Profit", "Profit_Margin_%": "Profit Margin (%)"
            },
        )

st.write("")

# ---- Category level ----
category_analysis = (
    df_filtered.groupby("Category Name", observed=True)
    .agg(
        Orders=("Order Profit Per Order", "size"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Order Profit Per Order", "sum"),
        Loss_Making_Orders=("Is_Loss", "sum"),
    )
    .reset_index()
)
category_analysis["Profit_Margin_%"] = np.where(
    category_analysis["Total_Sales"] > 0, category_analysis["Total_Profit"] / category_analysis["Total_Sales"] * 100, np.nan
)
category_analysis["Loss_Rate_%"] = category_analysis["Loss_Making_Orders"] / category_analysis["Orders"] * 100

MIN_ORDERS_CATEGORY = 20 if category_analysis["Orders"].max() > 60 else 1
category_reliable = category_analysis[category_analysis["Orders"] >= MIN_ORDERS_CATEGORY].copy()
if category_reliable.empty:
    category_reliable = category_analysis.copy()

# Analytical Category Risk Score: 55% loss rate + 45% inverse profit margin (normalized 0-100)
def normalize(series):
    lo, hi = series.min(), series.max()
    if hi - lo == 0:
        return pd.Series(0.0, index=series.index)
    return (series - lo) / (hi - lo) * 100


cat_risk = category_reliable.copy()
cat_risk["Loss_Rate_Norm"] = normalize(cat_risk["Loss_Rate_%"])
cat_risk["Inv_Margin_Norm"] = normalize(-cat_risk["Profit_Margin_%"])
cat_risk["Risk_Score"] = (0.55 * cat_risk["Loss_Rate_Norm"] + 0.45 * cat_risk["Inv_Margin_Norm"]).round(1)

col_c, col_d = st.columns(2)
with col_c:
    chart_card_open("Category Margin Leaders", f"Strongest categories by profit margin (min {MIN_ORDERS_CATEGORY} orders).")
    top_cats = category_reliable.sort_values("Profit_Margin_%", ascending=False).head(8)
    fig_cat = px.bar(
        top_cats.sort_values("Profit_Margin_%"),
        x="Profit_Margin_%",
        y="Category Name",
        orientation="h",
        color_discrete_sequence=[GREEN],
        text=top_cats.sort_values("Profit_Margin_%")["Profit_Margin_%"].round(2).astype(str) + "%",
    )
    fig_cat.update_traces(textposition="outside")
    fig_cat.update_layout(xaxis_title="Profit Margin (%)", yaxis_title="")
    st.plotly_chart(style_fig(fig_cat, height=360), use_container_width=True, key="chart_9")
    chart_card_close()

with col_d:
    chart_card_open("Category Profitability Heatmap", "Quickly spot strong vs. weak categories by profit margin.")
    heat_df = category_reliable.sort_values("Profit_Margin_%", ascending=False).head(20)
    fig_heat = px.imshow(
        heat_df[["Profit_Margin_%"]].T.values,
        x=heat_df["Category Name"],
        y=["Profit Margin (%)"],
        color_continuous_scale=["#F2545B", "#FFB020", "#8892A6", "#3DBFC8", "#3ED993"],
        aspect="auto",
        text_auto=".1f",
    )
    fig_heat.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(style_fig(fig_heat, height=290, legend=False), use_container_width=True, key="chart_10")
    chart_card_close()

col_e, col_f = st.columns(2)
with col_e:
    chart_card_open("Category Loss Rate", "Categories with the highest share of loss-making order items.")
    top_loss_cats = category_reliable.sort_values("Loss_Rate_%", ascending=False).head(8)
    fig_loss_cat = px.bar(
        top_loss_cats.sort_values("Loss_Rate_%"),
        x="Loss_Rate_%",
        y="Category Name",
        orientation="h",
        color_discrete_sequence=[RED],
        text=top_loss_cats.sort_values("Loss_Rate_%")["Loss_Rate_%"].round(2).astype(str) + "%",
    )
    fig_loss_cat.update_traces(textposition="outside")
    fig_loss_cat.update_layout(xaxis_title="Loss Rate (%)", yaxis_title="")
    st.plotly_chart(style_fig(fig_loss_cat, height=360), use_container_width=True, key="chart_11")
    chart_card_close()

with col_f:
    chart_card_open("Analytical Category Risk Score", "Composite of 55% loss rate + 45% inverse profit margin (0-100 scale).")
    top_risk_cats = cat_risk.sort_values("Risk_Score", ascending=False).head(8)
    fig_risk = px.bar(
        top_risk_cats.sort_values("Risk_Score"),
        x="Risk_Score",
        y="Category Name",
        orientation="h",
        color_discrete_sequence=[AMBER],
        text=top_risk_cats.sort_values("Risk_Score")["Risk_Score"],
    )
    fig_risk.update_traces(textposition="outside")
    fig_risk.update_layout(xaxis_title="Analytical Risk Score", yaxis_title="")
    st.plotly_chart(style_fig(fig_risk, height=360), use_container_width=True, key="chart_12")
    chart_card_close()

note(
    "The Analytical Category Risk Score is a dashboard-level analytical indicator "
    "(55% loss rate + 45% inverse profit margin), not an official APL Logistics KPI."
)

with st.expander("📋 View detailed category profitability &amp; risk table"):
    clean_table(
        cat_risk.sort_values("Total_Profit", ascending=False)[
            ["Category Name", "Orders", "Total_Sales", "Total_Profit", "Profit_Margin_%", "Loss_Rate_%", "Risk_Score"]
        ],
        rename_map={
            "Total_Sales": "Total Sales", "Total_Profit": "Total Profit",
            "Profit_Margin_%": "Profit Margin (%)", "Loss_Rate_%": "Loss Rate (%)", "Risk_Score": "Risk Score",
        },
        height=380,
    )

insight(
    "A small number of products and categories account for a disproportionate share of total profit. "
    "Use the tables above to separate consistently strong performers from categories that need pricing, "
    "cost, or discount-exposure review."
)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ============================================================================
# MODULE 04 — DISCOUNT IMPACT ANALYZER
# ============================================================================
section_header("04", "Discount Impact Analyzer", "Discounts can increase sales while silently reducing profitability.")

discount_analysis = (
    df_filtered.groupby("Discount_Band", observed=False)
    .agg(
        Order_Items=("Order Profit Per Order", "size"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Order Profit Per Order", "sum"),
        Avg_Profit_Ratio=("Order Item Profit Ratio", "mean"),
        Loss_Making_Items=("Is_Loss", "sum"),
    )
    .reindex(DISCOUNT_BAND_ORDER)
    .reset_index()
)
discount_analysis["Profit_Margin_%"] = np.where(
    discount_analysis["Total_Sales"] > 0, discount_analysis["Total_Profit"] / discount_analysis["Total_Sales"] * 100, np.nan
)
discount_analysis["Loss_Rate_%"] = np.where(
    discount_analysis["Order_Items"] > 0, discount_analysis["Loss_Making_Items"] / discount_analysis["Order_Items"] * 100, np.nan
)
discount_analysis["Avg_Profit_Ratio_%"] = discount_analysis["Avg_Profit_Ratio"] * 100

no_disc_sales = df_filtered.loc[df_filtered["Order Item Discount Rate"] == 0, "Sales"].sum()
no_disc_profit = df_filtered.loc[df_filtered["Order Item Discount Rate"] == 0, "Order Profit Per Order"].sum()
disc_sales = df_filtered.loc[df_filtered["Order Item Discount Rate"] > 0, "Sales"].sum()
disc_profit = df_filtered.loc[df_filtered["Order Item Discount Rate"] > 0, "Order Profit Per Order"].sum()
no_disc_margin_v = (no_disc_profit / no_disc_sales * 100) if no_disc_sales else np.nan
disc_margin_v = (disc_profit / disc_sales * 100) if disc_sales else np.nan
if no_disc_sales and disc_sales and no_disc_margin_v not in (0, np.nan) and not pd.isna(no_disc_margin_v) and no_disc_margin_v != 0:
    discount_impact_ratio = (no_disc_margin_v - disc_margin_v) / no_disc_margin_v * 100
else:
    discount_impact_ratio = np.nan

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card(
        "Discount Impact Ratio",
        fmt_pct(discount_impact_ratio) if not pd.isna(discount_impact_ratio) else "N/A",
        "Relative margin reduction vs. no-discount orders",
        "neg",
    )
with c2:
    kpi_card("No-Discount Margin", fmt_pct(no_disc_margin_v) if not pd.isna(no_disc_margin_v) else "N/A", "Baseline margin", "neutral")
with c3:
    kpi_card("Discounted Margin", fmt_pct(disc_margin_v) if not pd.isna(disc_margin_v) else "N/A", "Margin when discount > 0%", "neutral")
with c4:
    overall_loss_rate = df_filtered["Is_Loss"].mean() * 100
    kpi_card("Overall Loss Rate", fmt_pct(overall_loss_rate), "Share of loss-making order items", "neg")

note(
    "The Discount Impact Ratio expresses the <b>relative margin reduction</b> associated with discounted "
    "orders compared to non-discounted orders. It should not be interpreted as \"X% of profit was lost.\""
)

col_a, col_b = st.columns(2)
with col_a:
    chart_card_open("Margin &amp; Loss Rate by Discount Band")
    fig_dband = go.Figure()
    fig_dband.add_bar(
        x=discount_analysis["Discount_Band"], y=discount_analysis["Profit_Margin_%"],
        name="Profit Margin (%)", marker_color=BLUE,
    )
    fig_dband.add_scatter(
        x=discount_analysis["Discount_Band"], y=discount_analysis["Loss_Rate_%"],
        name="Loss Rate (%)", mode="lines+markers", line=dict(color=RED, width=3), yaxis="y2",
    )
    fig_dband.update_layout(
        yaxis=dict(title="Profit Margin (%)"),
        yaxis2=dict(title="Loss Rate (%)", overlaying="y", side="right", showgrid=False),
        xaxis_title="Discount Band",
    )
    st.plotly_chart(style_fig(fig_dband), use_container_width=True, key="chart_13")
    chart_card_close()

with col_b:
    chart_card_open("Average Profit Ratio by Discount Band")
    fig_apr = px.bar(
        discount_analysis,
        x="Discount_Band",
        y="Avg_Profit_Ratio_%",
        text=discount_analysis["Avg_Profit_Ratio_%"].round(2).astype(str) + "%",
        color_discrete_sequence=[PURPLE],
    )
    fig_apr.update_traces(textposition="outside")
    fig_apr.update_layout(xaxis_title="Discount Band", yaxis_title="Avg Profit Ratio (%)")
    st.plotly_chart(style_fig(fig_apr), use_container_width=True, key="chart_14")
    chart_card_close()

insight(
    f"Profit margin declines from <b>{fmt_pct(discount_analysis.loc[discount_analysis['Discount_Band']=='No Discount','Profit_Margin_%'].values[0]) if not discount_analysis.empty and not pd.isna(discount_analysis.loc[discount_analysis['Discount_Band']=='No Discount','Profit_Margin_%'].values[0]) else 'N/A'}</b> "
    f"without discount to lower levels at deeper discount bands, while the loss rate fluctuates rather than "
    f"increasing monotonically — margin pressure is the clearer signal than loss-rate escalation."
)

with st.expander("📋 View discount-band detail table"):
    clean_table(
        discount_analysis[
            ["Discount_Band", "Order_Items", "Total_Sales", "Total_Profit", "Profit_Margin_%", "Loss_Rate_%", "Avg_Profit_Ratio_%"]
        ],
        rename_map={
            "Discount_Band": "Discount Band", "Order_Items": "Order Items", "Total_Sales": "Total Sales",
            "Total_Profit": "Total Profit", "Profit_Margin_%": "Profit Margin (%)", "Loss_Rate_%": "Loss Rate (%)",
            "Avg_Profit_Ratio_%": "Avg Profit Ratio (%)",
        },
    )

# High-discount category analysis (20-25% band)
st.write("")
chart_card_open("High-Discount Category Analysis (20-25% Band)", "Categories with meaningful order volume and weak margins at deep discount.")
deep_band = df_filtered[df_filtered["Order Item Discount Rate"].between(0.20, 0.25, inclusive="both")]
if deep_band.empty:
    st.info("No order items fall within the 20-25% discount band for the current filter selection.")
else:
    deep_cat = (
        deep_band.groupby("Category Name", observed=True)
        .agg(Order_Items=("Order Profit Per Order", "size"), Total_Sales=("Sales", "sum"), Total_Profit=("Order Profit Per Order", "sum"))
        .reset_index()
    )
    deep_cat["Profit_Margin_%"] = np.where(deep_cat["Total_Sales"] > 0, deep_cat["Total_Profit"] / deep_cat["Total_Sales"] * 100, np.nan)
    min_orders_deep = 5 if deep_cat["Order_Items"].max() > 15 else 1
    deep_cat_reliable = deep_cat[deep_cat["Order_Items"] >= min_orders_deep].sort_values("Profit_Margin_%").head(10)
    if deep_cat_reliable.empty:
        deep_cat_reliable = deep_cat.sort_values("Profit_Margin_%").head(10)
    fig_deep = px.bar(
        deep_cat_reliable.sort_values("Profit_Margin_%", ascending=False),
        x="Category Name", y="Profit_Margin_%",
        color_discrete_sequence=[AMBER],
        text=deep_cat_reliable.sort_values("Profit_Margin_%", ascending=False)["Profit_Margin_%"].round(2).astype(str) + "%",
    )
    fig_deep.update_traces(textposition="outside")
    fig_deep.update_layout(xaxis_tickangle=-35, xaxis_title="", yaxis_title="Profit Margin (%) at 20-25% Discount")
    st.plotly_chart(style_fig(fig_deep, height=360), use_container_width=True, key="chart_15")
chart_card_close()

# What-if scenario
st.write("")
chart_card_open("Illustrative What-If Discount Scenario", "Exploratory only — not a forecast of actual profit.")
whatif_rate = st.slider("Select a hypothetical discount rate to apply to the current filtered pre-discount value", 0, 100, 10, step=1, key="whatif")
pre_discount_value = df_filtered["Order Item Product Price"].mul(df_filtered["Order Item Quantity"]).sum()
if pre_discount_value == 0:
    pre_discount_value = total_sales
estimated_discount_amount = pre_discount_value * whatif_rate / 100
estimated_revenue_after_discount = pre_discount_value - estimated_discount_amount

wc1, wc2, wc3 = st.columns(3)
with wc1:
    kpi_card("Pre-Discount Value", fmt_money(pre_discount_value), "Current filtered view", "neutral")
with wc2:
    kpi_card("Estimated Discount Amount", fmt_money(estimated_discount_amount), f"At {whatif_rate}% hypothetical rate", "neutral")
with wc3:
    kpi_card("Estimated Revenue After Discount", fmt_money(estimated_revenue_after_discount), "Illustrative only", "neutral")
chart_card_close()
note(
    "This what-if calculation is an <b>illustrative revenue scenario</b>, not a forecast of actual profit. "
    "It does not incorporate cost, shipping, or elasticity effects and should not be read as "
    "\"at X% discount, profit will be Y.\""
)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ============================================================================
# MODULE 05 — MARKET & REGIONAL ANALYSIS
# ============================================================================
section_header("05", "Market &amp; Regional Analysis", "Where is the business profitable — scale versus efficiency.")

market_analysis = (
    df_filtered.groupby("Market", observed=True)
    .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Order Profit Per Order", "sum"), Loss_Making_Orders=("Is_Loss", "sum"), Orders=("Order Profit Per Order", "size"))
    .reset_index()
)
market_analysis["Profit_Margin_%"] = np.where(market_analysis["Total_Sales"] > 0, market_analysis["Total_Profit"] / market_analysis["Total_Sales"] * 100, np.nan)
market_analysis["Loss_Rate_%"] = market_analysis["Loss_Making_Orders"] / market_analysis["Orders"] * 100
market_analysis["Profit_Contribution_%"] = market_analysis["Total_Profit"] / total_profit * 100 if total_profit else np.nan

col_a, col_b = st.columns(2)
with col_a:
    chart_card_open("Revenue vs Profit by Market", "Scale (sales) compared against actual profit generated per market.")
    fig_mkt = go.Figure()
    mkt_sorted = market_analysis.sort_values("Total_Sales", ascending=False)
    fig_mkt.add_bar(x=mkt_sorted["Market"], y=mkt_sorted["Total_Sales"], name="Revenue", marker_color=BLUE_SOFT)
    fig_mkt.add_bar(x=mkt_sorted["Market"], y=mkt_sorted["Total_Profit"], name="Profit", marker_color=GREEN)
    fig_mkt.update_layout(barmode="group", yaxis_title="Amount")
    st.plotly_chart(style_fig(fig_mkt), use_container_width=True, key="chart_16")
    chart_card_close()

with col_b:
    chart_card_open("Profit Margin &amp; Loss Rate by Market", "Highest margin market is not always the highest-scale market.")
    fig_mkt_margin = go.Figure()
    mkt_margin_sorted = market_analysis.sort_values("Profit_Margin_%", ascending=False)
    fig_mkt_margin.add_bar(x=mkt_margin_sorted["Market"], y=mkt_margin_sorted["Profit_Margin_%"], name="Profit Margin (%)", marker_color=BLUE)
    fig_mkt_margin.add_scatter(x=mkt_margin_sorted["Market"], y=mkt_margin_sorted["Loss_Rate_%"], name="Loss Rate (%)", mode="lines+markers", line=dict(color=RED, width=3), yaxis="y2")
    fig_mkt_margin.update_layout(yaxis=dict(title="Profit Margin (%)"), yaxis2=dict(title="Loss Rate (%)", overlaying="y", side="right", showgrid=False))
    st.plotly_chart(style_fig(fig_mkt_margin), use_container_width=True, key="chart_17")
    chart_card_close()

best_margin_row = market_analysis.sort_values("Profit_Margin_%", ascending=False).iloc[0] if not market_analysis.empty else None
best_scale_row = market_analysis.sort_values("Total_Sales", ascending=False).iloc[0] if not market_analysis.empty else None
if best_margin_row is not None and best_scale_row is not None:
    insight(
        f"<b>{best_scale_row['Market']}</b> leads in absolute scale ({fmt_money(best_scale_row['Total_Sales'])} in sales), "
        f"while <b>{best_margin_row['Market']}</b> shows the strongest margin efficiency "
        f"({fmt_pct(best_margin_row['Profit_Margin_%'])}) within the current view. Scale does not equal efficiency."
    )

# Regional analysis
region_analysis = (
    df_filtered.groupby("Order Region", observed=True)
    .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Order Profit Per Order", "sum"), Loss_Making_Orders=("Is_Loss", "sum"), Orders=("Order Profit Per Order", "size"))
    .reset_index()
)
region_analysis["Profit_Margin_%"] = np.where(region_analysis["Total_Sales"] > 0, region_analysis["Total_Profit"] / region_analysis["Total_Sales"] * 100, np.nan)
region_analysis["Loss_Rate_%"] = region_analysis["Loss_Making_Orders"] / region_analysis["Orders"] * 100
region_analysis["Profit_Contribution_%"] = region_analysis["Total_Profit"] / total_profit * 100 if total_profit else np.nan

MIN_ORDERS_REGION = 20 if region_analysis["Orders"].max() > 60 else 1
region_reliable = region_analysis[region_analysis["Orders"] >= MIN_ORDERS_REGION].copy()
if region_reliable.empty:
    region_reliable = region_analysis.copy()

col_c, col_d = st.columns(2)
with col_c:
    chart_card_open("Top Regions by Profit Margin", f"Regions with at least {MIN_ORDERS_REGION} orders in the current view.")
    top_regions = region_reliable.sort_values("Profit_Margin_%", ascending=False).head(8)
    fig_top_reg = px.bar(
        top_regions.sort_values("Profit_Margin_%"), x="Profit_Margin_%", y="Order Region", orientation="h",
        color_discrete_sequence=[GREEN], text=top_regions.sort_values("Profit_Margin_%")["Profit_Margin_%"].round(2).astype(str) + "%",
    )
    fig_top_reg.update_traces(textposition="outside")
    fig_top_reg.update_layout(xaxis_title="Profit Margin (%)", yaxis_title="")
    st.plotly_chart(style_fig(fig_top_reg, height=360), use_container_width=True, key="chart_18")
    chart_card_close()

with col_d:
    chart_card_open("Weakest Regions by Profit Margin", "Regions requiring review of pricing, discount, or cost exposure.")
    bottom_regions = region_reliable.sort_values("Profit_Margin_%", ascending=True).head(8)
    fig_bot_reg = px.bar(
        bottom_regions.sort_values("Profit_Margin_%", ascending=False), x="Profit_Margin_%", y="Order Region", orientation="h",
        color_discrete_sequence=[RED], text=bottom_regions.sort_values("Profit_Margin_%", ascending=False)["Profit_Margin_%"].round(2).astype(str) + "%",
    )
    fig_bot_reg.update_traces(textposition="outside")
    fig_bot_reg.update_layout(xaxis_title="Profit Margin (%)", yaxis_title="")
    st.plotly_chart(style_fig(fig_bot_reg, height=360), use_container_width=True, key="chart_19")
    chart_card_close()

# Country analysis (Customer Country — only where volume is sufficient)
country_analysis = (
    df_filtered.groupby("Customer Country", observed=True)
    .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Order Profit Per Order", "sum"), Loss_Making_Orders=("Is_Loss", "sum"), Orders=("Order Profit Per Order", "size"))
    .reset_index()
)
country_analysis["Profit_Margin_%"] = np.where(country_analysis["Total_Sales"] > 0, country_analysis["Total_Profit"] / country_analysis["Total_Sales"] * 100, np.nan)
country_analysis["Loss_Rate_%"] = country_analysis["Loss_Making_Orders"] / country_analysis["Orders"] * 100
country_analysis["Profit_Contribution_%"] = country_analysis["Total_Profit"] / total_profit * 100 if total_profit else np.nan
MIN_ORDERS_COUNTRY = 30
country_reliable = country_analysis[country_analysis["Orders"] >= MIN_ORDERS_COUNTRY].copy()

chart_card_open("Country Analysis (Customer Country)", f"Shown only where order volume is sufficient (≥ {MIN_ORDERS_COUNTRY} orders).")
if country_reliable.empty:
    st.info("No country in the current filtered view meets the minimum order-volume threshold for reliable reporting.")
else:
    fig_country = px.bar(
        country_reliable.sort_values("Total_Sales", ascending=False),
        x="Customer Country", y="Total_Sales", color="Profit_Margin_%",
        color_continuous_scale=["#F2545B", "#FFB020", "#3DBFC8", "#3ED993"],
        text=country_reliable.sort_values("Total_Sales", ascending=False)["Total_Sales"].map(lambda v: fmt_money(v)),
    )
    fig_country.update_traces(textposition="outside")
    fig_country.update_layout(xaxis_title="", yaxis_title="Total Sales")
    st.plotly_chart(style_fig(fig_country, height=340, legend=False), use_container_width=True, key="chart_20")
chart_card_close()

with st.expander("📋 View detailed Market / Region / Country tables"):
    tm, tr, tc = st.tabs(["Market", "Order Region", "Customer Country"])
    with tm:
        clean_table(
            market_analysis.sort_values("Total_Profit", ascending=False)[
                ["Market", "Total_Sales", "Total_Profit", "Profit_Margin_%", "Loss_Rate_%", "Profit_Contribution_%"]
            ],
            rename_map={
                "Total_Sales": "Total Sales", "Total_Profit": "Total Profit", "Profit_Margin_%": "Profit Margin (%)",
                "Loss_Rate_%": "Loss Rate (%)", "Profit_Contribution_%": "Profit Contribution (%)",
            },
        )
    with tr:
        clean_table(
            region_analysis.sort_values("Total_Profit", ascending=False)[
                ["Order Region", "Total_Sales", "Total_Profit", "Profit_Margin_%", "Loss_Rate_%", "Profit_Contribution_%"]
            ],
            rename_map={
                "Total_Sales": "Total Sales", "Total_Profit": "Total Profit", "Profit_Margin_%": "Profit Margin (%)",
                "Loss_Rate_%": "Loss Rate (%)", "Profit_Contribution_%": "Profit Contribution (%)",
            },
            height=360,
        )
    with tc:
        clean_table(
            country_analysis.sort_values("Total_Profit", ascending=False)[
                ["Customer Country", "Total_Sales", "Total_Profit", "Profit_Margin_%", "Loss_Rate_%", "Profit_Contribution_%"]
            ],
            rename_map={
                "Total_Sales": "Total Sales", "Total_Profit": "Total Profit", "Profit_Margin_%": "Profit Margin (%)",
                "Loss_Rate_%": "Loss Rate (%)", "Profit_Contribution_%": "Profit Contribution (%)",
            },
        )

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown(
    """
    <div class="footer-box">
        <b>APL Logistics • Profitability &amp; Supply Chain Intelligence Dashboard</b><br>
        Analytical views are based on the supplied dataset and should be interpreted as observational
        decision support. Findings describe observed associations, not proven causal effects. No order-date
        field exists in this dataset, so no chronological trend is implied. Currency is not specified in the
        source data. Customer Value Tiers and the Analytical Category Risk Score are dashboard-level
        analytical constructs, not official APL Logistics KPIs.
    </div>
    """,
    unsafe_allow_html=True,
)
