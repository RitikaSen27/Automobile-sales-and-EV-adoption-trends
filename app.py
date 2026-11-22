import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import os

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="India EV Adoption & Sales Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Design tokens (mint / glass look)
# ---------------------------------------------------------
GREEN = "#22C55E"
TEAL = "#14B8A6"
SKY = "#0EA5E9"
AMBER = "#F59E0B"
VIOLET = "#8B5CF6"
RED = "#EF4444"
INK = "#0F172A"
MUTED = "#64748B"
PALETTE = [GREEN, SKY, AMBER, VIOLET, TEAL, RED]

# Plotly: transparent background, soft grid, one consistent palette
pio.templates["ev_mint"] = go.layout.Template(
    layout=dict(
        colorway=PALETTE,
        font=dict(family="Plus Jakarta Sans, Inter, sans-serif", color=INK, size=13),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(font=dict(size=17, color=INK), x=0.02, xanchor="left"),
        xaxis=dict(gridcolor="rgba(15,23,42,0.07)", zerolinecolor="rgba(15,23,42,0.1)", linecolor="rgba(15,23,42,0.12)"),
        yaxis=dict(gridcolor="rgba(15,23,42,0.07)", zerolinecolor="rgba(15,23,42,0.1)", linecolor="rgba(15,23,42,0.12)"),
        hoverlabel=dict(bgcolor="white", font_size=13, font_color=INK),
    )
)
pio.templates.default = "ev_mint"


def show(fig, container=st):
    """Render a Plotly chart with consistent spacing and a legend that never overlaps the axis."""
    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, title_text=""),
    )
    container.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# Global CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp, .stMarkdown, button, input, select, textarea {
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
    }

    /* Page background: soft mint gradient */
    .stApp {
        background:
            radial-gradient(1200px 500px at 85% -10%, rgba(45,212,191,0.22), transparent 60%),
            radial-gradient(900px 500px at -5% 20%, rgba(34,197,94,0.14), transparent 60%),
            linear-gradient(135deg, #E9F5F2 0%, #DCEEEC 55%, #EAF4F2 100%);
        color: #0F172A;
    }
    header[data-testid="stHeader"] { background: transparent; }
    .block-container { padding-top: 2.2rem; max-width: 1280px; }

    /* Headings */
    h1, h2, h3 { color: #0F172A !important; letter-spacing: -0.02em; }
    h2 { font-weight: 800 !important; font-size: 1.9rem !important; }
    h3 { font-weight: 700 !important; }
    p, li { color: #334155; }

    /* ---------- Hero ---------- */
    .hero {
        position: relative;
        background: linear-gradient(135deg, rgba(255,255,255,0.92), rgba(255,255,255,0.6));
        border: 1px solid rgba(255,255,255,0.9);
        border-radius: 28px;
        padding: 30px 34px;
        box-shadow: 0 18px 50px rgba(15,118,110,0.12);
        overflow: hidden;
        margin-bottom: 22px;
    }
    .hero::after {
        content: "";
        position: absolute; right: -60px; top: -60px;
        width: 260px; height: 260px; border-radius: 50%;
        background: radial-gradient(circle, rgba(45,212,191,0.45), rgba(74,222,128,0.0) 70%);
    }
    .hero-eyebrow {
        display: inline-block;
        background: rgba(34,197,94,0.12); color: #15803D;
        font-weight: 700; font-size: 0.78rem; letter-spacing: 0.06em; text-transform: uppercase;
        padding: 5px 12px; border-radius: 999px; margin-bottom: 12px;
    }
    .hero-title {
        font-size: 2.7rem; line-height: 1.08; font-weight: 800; color: #0F172A;
        letter-spacing: -0.03em; margin: 0 0 10px 0; max-width: 760px;
    }
    .hero-sub { font-size: 1.02rem; color: #475569; max-width: 720px; margin: 0; }
    .hero-pills { margin-top: 18px; display: flex; flex-wrap: wrap; gap: 8px; position: relative; z-index: 1; }
    .hero-pill {
        background: linear-gradient(90deg, #2DD4BF, #4ADE80); color: #052e16;
        font-weight: 700; font-size: 0.82rem; padding: 8px 16px; border-radius: 999px;
        box-shadow: 0 6px 16px rgba(34,197,94,0.28);
    }
    .hero-pill.ghost { background: rgba(255,255,255,0.8); color: #0F172A; box-shadow: none; border: 1px solid rgba(15,23,42,0.08); }

    /* ---------- KPI cards ---------- */
    .metric-card {
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.95);
        border-radius: 22px;
        padding: 18px 18px 16px 18px;
        box-shadow: 0 10px 30px rgba(15,23,42,0.07);
        height: 100%;
    }
    .metric-icon {
        width: 38px; height: 38px; border-radius: 12px;
        background: linear-gradient(135deg, #CCFBF1, #BBF7D0);
        display: flex; align-items: center; justify-content: center; font-size: 1.15rem;
        margin-bottom: 12px;
    }
    .metric-lbl { font-size: 0.72rem; color: #64748B; text-transform: uppercase; font-weight: 700; letter-spacing: 0.06em; margin-bottom: 2px; }
    .metric-val { font-size: 1.9rem; font-weight: 800; color: #0F172A; letter-spacing: -0.02em; line-height: 1.15; }
    .metric-delta { font-size: 0.8rem; font-weight: 600; color: #15803D; margin-top: 4px; }
    .metric-bar { height: 8px; border-radius: 999px; background: rgba(15,23,42,0.08); margin-top: 12px; overflow: hidden; }
    .metric-bar > span { display: block; height: 100%; border-radius: 999px; background: linear-gradient(90deg, #2DD4BF, #4ADE80); }

    /* Archetype tags (kept for compatibility) */
    .tag-pioneer { background-color: #DBEAFE; color: #1E40AF; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 0.75rem; }
    .tag-deficit { background-color: #FEE2E2; color: #991B1B; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 0.75rem; }
    .tag-trans { background-color: #FEF3C7; color: #92400E; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 0.75rem; }
    .tag-industrial { background-color: #D1FAE5; color: #065F46; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 0.75rem; }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.78), rgba(236,253,245,0.7));
        backdrop-filter: blur(14px);
        border-right: 1px solid rgba(255,255,255,0.9);
    }
    section[data-testid="stSidebar"] > div { padding-top: 1.2rem; }
    .brand { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }
    .brand-logo {
        width: 44px; height: 44px; border-radius: 14px; font-size: 1.4rem;
        background: linear-gradient(135deg, #2DD4BF, #4ADE80);
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 8px 18px rgba(34,197,94,0.35);
    }
    .brand-name { font-weight: 800; font-size: 1.15rem; color: #0F172A; line-height: 1.1; }
    .brand-sub { font-size: 0.74rem; color: #64748B; font-weight: 600; }

    /* Navigation radio -> pill buttons */
    section[data-testid="stSidebar"] div[role="radiogroup"] { gap: 8px; }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        background: rgba(255,255,255,0.75);
        border: 1px solid rgba(15,23,42,0.06);
        border-radius: 16px;
        padding: 11px 14px;
        width: 100%;
        transition: all .15s ease;
        box-shadow: 0 2px 6px rgba(15,23,42,0.04);
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover { transform: translateX(2px); border-color: rgba(34,197,94,0.5); }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child { display: none; }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label p { font-weight: 600; font-size: 0.9rem; color: #0F172A; margin: 0; }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(90deg, #2DD4BF, #4ADE80);
        border-color: transparent;
        box-shadow: 0 8px 20px rgba(34,197,94,0.32);
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p { color: #052e16; font-weight: 800; }
    section[data-testid="stSidebar"] [data-testid="stAlert"] { border-radius: 16px; }

    /* ---------- Chart containers ---------- */
    div[data-testid="stPlotlyChart"] {
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.95);
        border-radius: 24px;
        padding: 10px 8px 4px 8px;
        box-shadow: 0 10px 30px rgba(15,23,42,0.07);
    }

    /* ---------- Native st.metric as cards ---------- */
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.85);
        border: 1px solid rgba(255,255,255,0.95);
        border-radius: 18px;
        padding: 14px 16px;
        box-shadow: 0 8px 22px rgba(15,23,42,0.06);
    }
    div[data-testid="stMetricLabel"] p { font-size: 0.74rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; }
    div[data-testid="stMetricValue"] { font-weight: 800; color: #0F172A; }

    /* ---------- Inputs ---------- */
    div[data-baseweb="select"] > div { border-radius: 14px !important; background: rgba(255,255,255,0.9) !important; border-color: rgba(15,23,42,0.08) !important; }
    div[data-testid="stSlider"] [role="slider"] { background: #22C55E !important; box-shadow: 0 0 0 4px rgba(34,197,94,0.2) !important; }
    button[role="tab"] { font-weight: 700; border-radius: 12px 12px 0 0; }
    button[role="tab"][aria-selected="true"] { color: #15803D; }
    div[data-baseweb="tab-highlight"] { background-color: #22C55E !important; }

    /* ---------- Alerts / info boxes ---------- */
    div[data-testid="stAlert"] { border-radius: 18px; border: 1px solid rgba(255,255,255,0.9); box-shadow: 0 8px 22px rgba(15,23,42,0.05); }

    hr { border-color: rgba(15,23,42,0.08) !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Loader
# ---------------------------------------------------------
@st.cache_data
def load_all_data():
    clean_dir = "clean"
    tables = {}
    if os.path.exists(clean_dir):
        for f in os.listdir(clean_dir):
            if f.endswith(".csv"):
                tables[f.replace(".csv", "")] = pd.read_csv(os.path.join(clean_dir, f))
    return tables

tables = load_all_data()

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
st.sidebar.markdown(
    '<div class="brand"><div class="brand-logo">⚡</div>'
    '<div><div class="brand-name">EV India</div><div class="brand-sub">Adoption Analytics</div></div></div>',
    unsafe_allow_html=True,
)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

menu_choice = st.sidebar.radio(
    "Select Analysis Module:",
    [
        "📊 Executive Dashboard & Trends",
        "🗺️ State Analytics & Archetypes",
        "🥊 State Benchmarking Tool",
        "💰 Interactive TCO Simulator",
        "🏛️ Subsidy Efficacy & Capital Efficiency",
        "🔮 2030 Adoption S-Curve Forecasting",
        "🎯 Strategic Stakeholder Playbooks"
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Data Source:** Official Rajya Sabha parliamentary questions (40 source CSVs) + MoHFW/Census population projections + RBI/MoSPI GSDP per capita."
)

# ---------------------------------------------------------
# Hero header
# ---------------------------------------------------------
st.markdown("""
<div class="hero">
    <span class="hero-eyebrow">India · EV Market Intelligence</span>
    <div class="hero-title">Smart EV Insights,<br>Made Simple</div>
    <p class="hero-sub">Macro trends, state archetypes, cost-of-ownership parity, policy mechanics and 2030 forecasts, all in one place.</p>
    <div class="hero-pills">
        <span class="hero-pill">7 analysis modules</span>
        <span class="hero-pill ghost">34 states &amp; UTs</span>
        <span class="hero-pill ghost">Rajya Sabha official data</span>
    </div>
</div>
""", unsafe_allow_html=True)


def kpi_card(icon, label, value, sub, bar=None):
    bar_html = f'<div class="metric-bar"><span style="width:{bar}%"></span></div>' if bar is not None else ""
    return (
        f'<div class="metric-card"><div class="metric-icon">{icon}</div>'
        f'<div class="metric-lbl">{label}</div><div class="metric-val">{value}</div>'
        f'<div class="metric-delta">{sub}</div>{bar_html}</div>'
    )


# Top KPI Summary Cards
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.markdown(kpi_card("🚗", "Total Registered EVs", "1.68M+", "FY24 Annualized (VAHAN)"), unsafe_allow_html=True)
kpi2.markdown(kpi_card("🛺", "3W EV Market Share", "52.4%", "Commercial Lead Segment", bar=52.4), unsafe_allow_html=True)
kpi3.markdown(kpi_card("🔌", "Public Chargers (EVPCS)", "12,146", "MoP Disclosed Count"), unsafe_allow_html=True)
kpi4.markdown(kpi_card("⏱️", "3W TCO Payback", "3.7 Mos", "Instant Fuel Arbitrage"), unsafe_allow_html=True)
kpi5.markdown(kpi_card("📈", "Projected 2030 3W Share", "88.2%", "Beats NITI 80% Target", bar=88.2), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# 1. EXECUTIVE DASHBOARD & TRENDS
# ---------------------------------------------------------
if menu_choice == "📊 Executive Dashboard & Trends":
    st.header("1. National Registration Growth & Segment Breakdown")
    
    col_left, col_right = st.columns([1, 1])
    
    # Category trends
    df_cat = tables.get("ev_registration_by_category", pd.DataFrame()).copy()
    if not df_cat.empty:
        df_cat["year_sort"] = df_cat["year"].astype(str).str.extract(r'(\d{4})')[0].astype(int)
        
        fig_cat = px.line(
            df_cat.sort_values("year_sort"),
            x="year_sort",
            y="ev_pct",
            color="vehicle_category",
            markers=True,
            title="EV Adoption Penetration (%) by Vehicle Category (2018–2023)",
            labels={"year_sort": "Year", "ev_pct": "EV Share of Total Fleet (%)", "vehicle_category": "Category"},
            color_discrete_sequence=PALETTE
        )
        fig_cat.update_layout(hovermode="x unified")
        show(fig_cat, col_left)
    
    # Global comparison
    df_global = tables.get("global_ev_share", pd.DataFrame()).copy()
    if not df_global.empty:
        df_global["year_sort"] = df_global["year"].astype(int)
        fig_global = px.bar(
            df_global.sort_values("year_sort"),
            x="year_sort",
            y="market_share_pct",
            color="Region",
            barmode="stack",
            title="Global EV Market Composition by Region (2019–2023)",
            labels={"year_sort": "Year", "market_share_pct": "Market Share (%)"},
            color_discrete_sequence=[RED, SKY, GREEN, VIOLET]
        )
        fig_global.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
        show(fig_global, col_right)
        
    st.markdown("### Key Analytical Insights")
    st.markdown("""
    - **India's EV transition is a Three-Wheeler story first:** Electric 3-wheelers rose from **14.4% in 2018 to >52.4% in 2023**, catalyzed by daily commercial mileage fuel savings in last-mile transport (e-rickshaws, cargo).
    - **Two-Wheelers follow steadily:** 2W EV share accelerated from 0.09% in 2018 to **5.28% in 2023**, reaching inflection with improved model availability.
    - **Four-Wheelers (Cars) remain stuck under 2%:** Constrained by high upfront battery pack costs and lower personal daily running mileage.
    - **Global Context:** India's rapid acceleration mirrors Europe's market share expansion (from 2.9% to 18.8%) as the global market diversifies away from early Chinese dominance (dropping from 93.2% to 68.2%).
    """)

# ---------------------------------------------------------
# 2. STATE ANALYTICS & ARCHETYPES
# ---------------------------------------------------------
elif menu_choice == "🗺️ State Analytics & Archetypes":
    st.header("2. State-Level Disparities, Infrastructure Adequacy & Clustering")
    
    df_state = tables.get("state_ev_enriched", pd.DataFrame()).copy()
    
    if not df_state.empty:
        # Toggle view
        sort_metric = st.selectbox(
            "Sort State Ranking By:",
            ["EV Penetration Rate (% of Fleet)", "EV Count (Absolute)", "EVs per 100k Population", "Charging Infrastructure Adequacy Ratio (CIAR)", "Public Chargers Count"]
        )
        
        metric_map = {
            "EV Penetration Rate (% of Fleet)": "ev_penetration_pct",
            "EV Count (Absolute)": "ev_count",
            "EVs per 100k Population": "ev_per_100k_pop",
            "Charging Infrastructure Adequacy Ratio (CIAR)": "ciar",
            "Public Chargers Count": "chargers"
        }
        
        col_chart, col_scat = st.columns([1, 1])
        
        top15_state = df_state.sort_values(metric_map[sort_metric], ascending=False).head(15)
        
        fig_bar = px.bar(
            top15_state,
            x=metric_map[sort_metric],
            y="state",
            orientation="h",
            color="cluster_id",
            title=f"Top 15 States by {sort_metric}",
            labels={metric_map[sort_metric]: sort_metric, "state": "State", "cluster_id": "Cluster ID"},
            color_continuous_scale="Viridis"
        )
        fig_bar.update_layout(yaxis=dict(autorange="reversed"))
        show(fig_bar, col_chart)
        
        # Archetype Scatter
        fig_scat = px.scatter(
            df_state,
            x="ev_penetration_pct",
            y="chargers_per_100k_pop",
            size="ev_count",
            color="archetype" if "archetype" in df_state.columns else "cluster_id",
            hover_name="state",
            hover_data=["ev_count", "chargers", "ciar", "pct_3w", "gsdp_pc_inr"],
            title="K-Means Market Archetypes: Fleet Penetration vs. Charger Density",
            labels={
                "ev_penetration_pct": "EV Penetration Rate (% of Fleet)",
                "chargers_per_100k_pop": "Public Chargers per 100k Pop",
                "archetype": "Market Archetype"
            }
        )
        show(fig_scat, col_scat)
        
        # CIAR Benchmarking Section
        st.subheader("Charging Infrastructure Adequacy Ratio (CIAR) vs. IEA 10:1 Benchmark")
        st.markdown(
            "The **International Energy Agency (IEA)** recommends **10 EVs per public charger**. "
            "Ratios exceeding 50:1 signal emerging strain, while >150:1 represents severe infrastructure deficit."
        )
        
        df_ciar_chart = df_state[df_state["ev_count"] >= 500].sort_values("ciar", ascending=False)
        fig_ciar = go.Figure()
        
        fig_ciar.add_trace(go.Bar(
            y=df_ciar_chart["state"],
            x=df_ciar_chart["ciar"],
            orientation='h',
            marker=dict(
                color=df_ciar_chart["ciar"],
                colorscale="Reds",
                showscale=True
            ),
            text=df_ciar_chart["ciar"].apply(lambda v: f"{v:.0f}:1"),
            textposition='outside'
        ))
        
        # Benchmark lines
        fig_ciar.add_vline(x=10, line_dash="dash", line_color="blue", annotation_text="IEA Target (10:1)")
        fig_ciar.add_vline(x=50, line_dash="dot", line_color="orange", annotation_text="Moderate Strain (50:1)")
        fig_ciar.add_vline(x=150, line_dash="dashdot", line_color="red", annotation_text="Acute Deficit (150:1)")
        
        fig_ciar.update_layout(
            height=700,
            xaxis_title="EVs per Public Charging Station (Log Scale)",
            xaxis_type="log",
            yaxis=dict(autorange="reversed")
        )
        show(fig_ciar, st)

# ---------------------------------------------------------
# 3. STATE BENCHMARKING TOOL
# ---------------------------------------------------------
elif menu_choice == "🥊 State Benchmarking Tool":
    st.header("3. Head-to-Head State EV Maturity Benchmarking")
    st.markdown("Compare any two Indian states/UTs side-by-side across fleet scale, charger adequacy, per-capita adoption, and economic indicators.")
    
    df_state = tables.get("state_ev_enriched", pd.DataFrame()).copy()
    
    if not df_state.empty:
        all_states = sorted(df_state["state"].unique())
        
        col_s1, col_s2 = st.columns(2)
        state_a = col_s1.selectbox("Select State A:", all_states, index=all_states.index("Uttar Pradesh") if "Uttar Pradesh" in all_states else 0)
        state_b = col_s2.selectbox("Select State B:", all_states, index=all_states.index("Karnataka") if "Karnataka" in all_states else 1)
        
        row_a = df_state[df_state["state"] == state_a].iloc[0]
        row_b = df_state[df_state["state"] == state_b].iloc[0]
        
        # Display side-by-side metrics
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        
        with m1:
            st.metric("Total EVs", f"{int(row_a['ev_count']):,}", f"{state_b}: {int(row_b['ev_count']):,}", delta_color="off")
        with m2:
            st.metric("EV Penetration %", f"{row_a['ev_penetration_pct']:.2f}%", f"{state_b}: {row_b['ev_penetration_pct']:.2f}%", delta_color="off")
        with m3:
            st.metric("Public Chargers", f"{int(row_a['chargers']):,}", f"{state_b}: {int(row_b['chargers']):,}", delta_color="off")
        with m4:
            st.metric("CIAR (EVs/Charger)", f"{row_a['ciar']:.1f}", f"{state_b}: {row_b['ciar']:.1f}", delta_color="off")
        with m5:
            st.metric("3W Fleet Share %", f"{row_a['pct_3w']:.1f}%", f"{state_b}: {row_b['pct_3w']:.1f}%", delta_color="off")
        with m6:
            st.metric("GSDP per Capita", f"₹{int(row_a['gsdp_pc_inr']):,}", f"{state_b}: ₹{int(row_b['gsdp_pc_inr']):,}", delta_color="off")
            
        st.markdown("---")
        
        # Comparison radar or bar
        comp_df = pd.DataFrame({
            "Metric": ["EV Penetration (%)", "Chargers per 100k Pop", "3W Share (%)", "2W Share (%)", "4W Share (%)"],
            state_a: [row_a["ev_penetration_pct"], row_a["chargers_per_100k_pop"], row_a["pct_3w"], row_a["pct_2w"], row_a["pct_4w"]],
            state_b: [row_b["ev_penetration_pct"], row_b["chargers_per_100k_pop"], row_b["pct_3w"], row_b["pct_2w"], row_b["pct_4w"]]
        })
        
        fig_comp = px.bar(
            comp_df.melt(id_vars="Metric", var_name="State", value_name="Value"),
            x="Metric",
            y="Value",
            color="State",
            barmode="group",
            title=f"Head-to-Head Comparison: {state_a} vs. {state_b}",
            color_discrete_sequence=[GREEN, SKY]
        )
        show(fig_comp, st)
        
        st.info(
            f"**Strategic Takeaway:** **{state_a}** operates as **{row_a.get('archetype', 'Cluster ' + str(row_a.get('cluster_id')))}** "
            f"with a charger deficit of **{int(row_a.get('chargers_needed_iea_10_1', 0)):,} chargers** to reach IEA adequacy. "
            f"In contrast, **{state_b}** operates as **{row_b.get('archetype', 'Cluster ' + str(row_b.get('cluster_id')))}**."
        )

# ---------------------------------------------------------
# 4. INTERACTIVE TCO SIMULATOR
# ---------------------------------------------------------
elif menu_choice == "💰 Interactive TCO Simulator":
    st.header("4. Total Cost of Ownership (TCO) Simulator & Payback Calculator")
    st.markdown("Customize daily driving distance, fuel rates, and electricity tariffs to calculate live financial breakeven periods and savings.")
    
    sim_col1, sim_col2 = st.columns([1, 2])
    
    with sim_col1:
        st.subheader("Vehicle & Operating Assumptions")
        sim_seg = st.selectbox("Vehicle Segment:", ["Commercial 3-Wheeler (Auto)", "Personal 2-Wheeler (Scooter)", "Personal 4-Wheeler (Passenger Car)"])
        
        if "3-Wheeler" in sim_seg:
            default_km = 110
            default_ice_price = 240000
            default_ev_price = 280000
            fuel_type = "CNG (₹/kg)"
            default_fuel_rate = 85.0
            fuel_eff = 25.0 # km/kg
            ev_eff = 55.0 # Wh/km
            ice_maint = 16000
            ev_maint = 6000
        elif "2-Wheeler" in sim_seg:
            default_km = 25
            default_ice_price = 90000
            default_ev_price = 125000
            fuel_type = "Petrol (₹/L)"
            default_fuel_rate = 100.0
            fuel_eff = 45.0 # km/L
            ev_eff = 30.0 # Wh/km
            ice_maint = 3500
            ev_maint = 1200
        else:
            default_km = 33
            default_ice_price = 1150000
            default_ev_price = 1600000
            fuel_type = "Petrol (₹/L)"
            default_fuel_rate = 100.0
            fuel_eff = 15.0 # km/L
            ev_eff = 140.0 # Wh/km
            ice_maint = 10000
            ev_maint = 4500
            
        daily_km_input = st.slider("Daily Driving Distance (km/day):", min_value=10, max_value=200, value=default_km, step=5)
        fuel_rate_input = st.slider(f"Fuel Price - {fuel_type}:", min_value=60.0, max_value=140.0, value=default_fuel_rate, step=1.0)
        elec_rate_input = st.slider("Electricity Tariff (₹/kWh):", min_value=4.0, max_value=15.0, value=7.5, step=0.5)
        capex_premium_input = st.slider("EV Upfront Price Premium (₹):", min_value=10000, max_value=600000, value=default_ev_price - default_ice_price, step=5000)
        
    with sim_col2:
        st.subheader("Live Economic Payback Results")
        
        annual_km = daily_km_input * 365
        ice_cost_per_km = fuel_rate_input / fuel_eff
        ev_cost_per_km = (ev_eff / 1000.0) * elec_rate_input
        annual_fuel_saving = (ice_cost_per_km - ev_cost_per_km) * annual_km
        annual_maint_saving = ice_maint - ev_maint
        total_annual_saving = annual_fuel_saving + annual_maint_saving
        
        payback_months = (capex_premium_input / total_annual_saving) * 12.0 if total_annual_saving > 0 else 999
        net_3yr = (total_annual_saving * 3) - capex_premium_input
        net_5yr = (total_annual_saving * 5) - capex_premium_input
        
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Running Cost (ICE)", f"₹{ice_cost_per_km:.2f}/km")
        r2.metric("Running Cost (EV)", f"₹{ev_cost_per_km:.2f}/km", f"-₹{ice_cost_per_km - ev_cost_per_km:.2f}/km")
        r3.metric("Payback Period", f"{payback_months:.1f} Months")
        r4.metric("3-Yr Net Cash Savings", f"₹{net_3yr:,.0f}")
        
        # Crossover Chart
        months = np.arange(0, 61)
        ice_cum = default_ice_price + (months / 12.0) * (ice_cost_per_km * annual_km + ice_maint)
        ev_cum = (default_ice_price + capex_premium_input) + (months / 12.0) * (ev_cost_per_km * annual_km + ev_maint)
        
        df_curve = pd.DataFrame({"Month": months, "ICE Cumulative TCO": ice_cum, "EV Cumulative TCO": ev_cum})
        
        fig_cross = go.Figure()
        fig_cross.add_trace(go.Scatter(x=df_curve["Month"], y=df_curve["ICE Cumulative TCO"], name="ICE Cumulative TCO", line=dict(color="#EF4444", width=2.5)))
        fig_cross.add_trace(go.Scatter(x=df_curve["Month"], y=df_curve["EV Cumulative TCO"], name="EV Cumulative TCO", line=dict(color="#10B981", width=2.5)))
        
        if payback_months <= 60:
            crossover_val = (default_ice_price + capex_premium_input) + (payback_months / 12.0) * (ev_cost_per_km * annual_km + ev_maint)
            fig_cross.add_trace(go.Scatter(
                x=[payback_months],
                y=[crossover_val],
                mode="markers+text",
                marker=dict(size=12, color="blue"),
                text=[f"Breakeven: {payback_months:.1f}m"],
                textposition="top center",
                name="Breakeven Point"
            ))
            
        fig_cross.update_layout(
            title=f"Cumulative Cost Crossover: ICE vs. EV ({sim_seg})",
            xaxis_title="Operating Timeline (Months)",
            yaxis_title="Total Expenditure (₹)",
            hovermode="x unified"
        )
        show(fig_cross, st)

# ---------------------------------------------------------
# 5. SUBSIDY EFFICACY & POLICY FRICTION
# ---------------------------------------------------------
elif menu_choice == "🏛️ Subsidy Efficacy & Capital Efficiency":
    st.header("5. FAME Scheme Fiscal Utilization & Policy Friction Analysis")
    
    df_policy = tables.get("subsidy_efficiency_analysis", pd.DataFrame()).copy()
    df_targets = tables.get("scheme_vehicle_targets", pd.DataFrame()).copy()
    df_subsidy = tables.get("scheme_subsidy_amount", pd.DataFrame()).copy()
    
    if not df_policy.empty:
        col_bud, col_eff = st.columns([1, 1])
        
        fig_bud = go.Figure()
        fig_bud.add_trace(go.Bar(
            x=df_policy["financial_year"],
            y=df_policy["budget_allocation_cr"],
            name="Budget Allocation (₹ Cr)",
            marker_color="#94A3B8"
        ))
        fig_bud.add_trace(go.Bar(
            x=df_policy["financial_year"],
            y=df_policy["fund_utilization_cr"],
            name="Fund Utilization (₹ Cr)",
            marker_color=GREEN
        ))
        fig_bud.add_trace(go.Scatter(
            x=df_policy["financial_year"],
            y=df_policy["utilization_pct"],
            name="Utilization Rate (%)",
            yaxis="y2",
            line=dict(color="#DC2626", width=3),
            mode="lines+markers"
        ))
        
        fig_bud.update_layout(title="Budget Allocation vs. Utilization & The 2023-24 Drop", yaxis=dict(title="Amount (₹ Crore)"), yaxis2=dict(title="Utilization Rate (%)", overlaying="y", side="right", range=[0, 115]), barmode="group")
        show(fig_bud, col_bud)
        
        # Capital intensity
        if not df_targets.empty and not df_subsidy.empty:
            cat_map = {"e-2 Wheelers": "e-2W", "e-3 Wheelers": "e-3W", "e-4 Wheelers": "e-4W", "e-buses": "e-Buses"}
            df_sub_copy = df_subsidy.copy()
            df_sub_copy["Category"] = df_sub_copy["Category"].replace(cat_map)
            m_eff = df_targets.merge(df_sub_copy, on="Category", how="inner")
            m_eff["spend_per_vehicle_inr"] = (m_eff["amount_rs_crore"] * 1e7) / m_eff["actual_vehicles"]
            m_eff["target_achievement_pct"] = (m_eff["actual_vehicles"] / m_eff["target_vehicles"]) * 100
            
            fig_eff = px.bar(
                m_eff,
                x="Category",
                y="spend_per_vehicle_inr",
                color="target_achievement_pct",
                title="Subsidy Spend per EV Deployed vs. Target Achievement (%)",
                labels={"spend_per_vehicle_inr": "Subsidy Spend per Vehicle (₹)", "target_achievement_pct": "Target Achieved (%)"},
                text=m_eff["spend_per_vehicle_inr"].apply(lambda v: f"₹{v:,.0f}"),
                color_continuous_scale="Tealgrn"
            )
            fig_eff.update_layout(yaxis_type="log")
            show(fig_eff, col_eff)
            
        st.markdown("### Structural Drivers of the 2023–24 Subsidy Utilization Drop")
        st.markdown("""
        1. **Phased Manufacturing Programme (PMP) Crackdown:** Government investigations in 2022–2023 discovered leading e-2W OEMs importing powertrain parts from China while claiming domestic subsidies. The Ministry froze subsidy disbursements and issued ₹500+ Cr clawback notices, freezing claims for months.
        2. **June 2023 Subsidy Reduction:** 2W subsidies were slashed from **₹15,000/kWh to ₹10,000/kWh** with maximum ex-factory cap lowered from 40% to 15%. This sparked an overnight price hike of ₹25,000–₹35,000 per vehicle, suppressing claim demand.
        3. **Capital Disparity:** e-2W disbursed **₹31,094 per vehicle** achieving **79.3% of target**, while e-4W absorbed **₹1.68 lakh per vehicle** yet achieved only **12.4% of target**. 1 electric bus consumed the public subsidy of **~90 electric two-wheelers**.
        """)

# ---------------------------------------------------------
# 6. 2030 ADOPTION FORECASTING
# ---------------------------------------------------------
elif menu_choice == "🔮 2030 Adoption S-Curve Forecasting":
    st.header("6. Technology Adoption S-Curve Forecasting (2018–2030)")
    st.markdown("Logistic diffusion curves (Bass Diffusion framework) calibrated against historical 2018–2023 sales data, benchmarked against NITI Aayog 2030 targets.")
    
    df_proj = tables.get("ev_adoption_projections_2030", pd.DataFrame()).copy()
    
    if not df_proj.empty:
        fig_proj = go.Figure()
        
        # Projections
        fig_proj.add_trace(go.Scatter(x=df_proj["year"], y=df_proj["three_wheeler_ev_pct"], name="3W S-Curve Projection", line=dict(color="#10B981", width=3)))
        fig_proj.add_trace(go.Scatter(x=df_proj["year"], y=df_proj["two_wheeler_ev_pct"], name="2W S-Curve Projection", line=dict(color="#3B82F6", width=3)))
        fig_proj.add_trace(go.Scatter(x=df_proj["year"], y=df_proj["four_wheeler_ev_pct"], name="4W S-Curve Projection", line=dict(color="#F59E0B", width=3)))
        
        # Targets
        fig_proj.add_hline(y=80, line_dash="dash", line_color="gray", annotation_text="NITI Aayog 2030 Target: 2W & 3W (80%)")
        fig_proj.add_hline(y=30, line_dash="dot", line_color="orange", annotation_text="NITI Aayog 2030 Target: 4W (30%)")
        
        fig_proj.update_layout(
            title="India EV Adoption S-Curve Projections (2018–2030) vs. NITI Aayog Targets",
            xaxis_title="Year",
            yaxis_title="EV Sales Penetration Rate (%)",
            xaxis=dict(tickmode="linear", tick0=2018, dtick=1),
            yaxis=dict(range=[0, 100]),
            hovermode="x unified"
        )
        show(fig_proj, st)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.success("### 3W: 88.2% by 2030\n**Ahead of Target:** Crosses NITI 80% threshold by 2026–2027 driven by immediate TCO payback.")
        with c2:
            st.info("### 2W: 71.8% by 2030\n**Close to Target:** Surges from 5.6% (2023) to 42.7% (2027) as battery costs decline; narrow 8% gap.")
        with c3:
            st.warning("### 4W: 28.8% by 2030\n**On Track:** Hits 14.1% by 2026 and reaches ~29% by 2030 as sub-₹12 lakh compact EVs arrive.")

# ---------------------------------------------------------
# 7. STRATEGIC PLAYBOOKS
# ---------------------------------------------------------
elif menu_choice == "🎯 Strategic Stakeholder Playbooks":
    st.header("7. Actionable Executive Strategy Playbooks")
    
    t_oem, t_cpo, t_policy = st.tabs(["🚗 Automobile OEMs", "🔌 Charging Point Operators (CPOs)", "🏛️ Policymakers & Regulators"])
    
    with t_oem:
        st.subheader("Playbook for Automobile Manufacturers (Tata, Mahindra, Ola, Ather, Bajaj)")
        st.markdown("""
        * **1. Prioritize Commercial 3W & B2B 2W Cargo:**
          * Unit economics and fuel arbitrage produce self-sustaining customer demand independent of consumer subsidies.
          * Embed factory-fitted IoT telematics and battery state-of-health tracking to lower NBFC lending risk and financing rates.
        * **2. The Sub-₹12 Lakh Mass-Market 4W Imperative:**
          * 80% of Indian personal passenger car sales occur below ₹12 lakh. Premium ₹25+ lakh EVs address only 5% of the market.
          * Develop compact LFP-battery hatchbacks and crossovers in the ₹8–12 lakh bracket to crack mass consumer adoption.
        * **3. Battery-as-a-Service (BaaS) & Swapping Partnerships:**
          * In high-CIAR states (UP, Bihar, Assam) where fixed fast chargers are scarce, partner with battery-swapping networks to drop upfront vehicle sticker prices by 40%.
        """)
        
    with t_cpo:
        st.subheader("Playbook for Charging Point Operators & Energy Utilities")
        st.markdown("""
        * **1. Capital Re-allocation (Geographic Arbitrage):**
          * CPOs have heavily over-indexed on already well-supplied hubs (Bengaluru, Mumbai, Pune).
          * High-density commercial transit corridors across UP, Bihar, and Rajasthan suffer acute charger deficits (>280–460 EVs per charger) representing massive unserved revenue.
        * **2. Dedicated Commercial Night Tariffs & Grid Load Management:**
          * Informal e-rickshaw overnight charging strains local distribution transformers.
          * CPOs and utilities must offer automated off-peak commercial EV charging tariffs at municipal depots to prevent transformer burnouts and balance the grid.
        """)
        
    with t_policy:
        st.subheader("Playbook for Ministry of Heavy Industries, NITI Aayog & MoRTH")
        st.markdown("""
        * **1. PM E-DRIVE Subsidy Reform:**
          * Transition from direct purchase capex subsidies (which caused the 38% utilization collapse in FY24) to **first-loss credit guarantees (FLCG) and interest rate subvention** via SIDBI.
        * **2. Mandated State CIAR Targets:**
          * Tie federal highway and municipal infrastructure grants to state CIAR thresholds (<25 EVs per public charger).
        * **3. National Battery Swapping Standardization:**
          * Finalize the draft National Battery Swapping Policy to standardize battery pack dimensions and communication protocols, preventing proprietary vendor lock-in.
        """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #9CA3AF; font-size: 0.85rem;'>"
    "⚡ Automobile Sales and EV Adoption Trends Analytics Platform | Built with Streamlit, Plotly & Python"
    "</div>",
    unsafe_allow_html=True
)