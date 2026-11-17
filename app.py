import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="India EV Adoption & Sales Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished aesthetics
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #111827;
    }
    .metric-lbl {
        font-size: 0.85rem;
        color: #6B7280;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .metric-delta {
        font-size: 0.82rem;
        font-weight: 600;
        color: #059669;
    }
    .tag-pioneer { background-color: #DBEAFE; color: #1E40AF; padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 0.75rem; }
    .tag-deficit { background-color: #FEE2E2; color: #991B1B; padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 0.75rem; }
    .tag-trans { background-color: #FEF3C7; color: #92400E; padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 0.75rem; }
    .tag-industrial { background-color: #D1FAE5; color: #065F46; padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 0.75rem; }
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
st.sidebar.image("https://img.icons8.com/fluency/96/electric-vehicle.png", width=64)
st.sidebar.title("Navigation")

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
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Data Source:** Official Rajya Sabha parliamentary questions (40 source CSVs) + MoHFW/Census population projections + RBI/MoSPI GSDP per capita."
)

# ---------------------------------------------------------
# Top Header Banner
# ---------------------------------------------------------
st.markdown('<div class="main-title">⚡ India Electric Vehicle Adoption & Market Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">End-to-End Business Analytics Platform: Macro Trends, Geographic Archetypes, TCO Parity, Policy Mechanics & 2030 Forecasting</div>', unsafe_allow_html=True)

# Top KPI Summary Cards
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    st.markdown('<div class="metric-card"><div class="metric-lbl">Total Registered EVs</div><div class="metric-val">1.68M+</div><div class="metric-delta">FY24 Annualized (VAHAN)</div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown('<div class="metric-card"><div class="metric-lbl">3W EV Market Share</div><div class="metric-val">52.4%</div><div class="metric-delta">Commercial Lead Segment</div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown('<div class="metric-card"><div class="metric-lbl">Public Chargers (EVPCS)</div><div class="metric-val">12,146</div><div class="metric-delta">MoP Disclosed Count</div></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown('<div class="metric-card"><div class="metric-lbl">3W TCO Payback</div><div class="metric-val">3.7 Mos</div><div class="metric-delta">Instant Fuel Arbitrage</div></div>', unsafe_allow_html=True)
with kpi5:
    st.markdown('<div class="metric-card"><div class="metric-lbl">Projected 2030 3W Share</div><div class="metric-val">88.2%</div><div class="metric-delta">Beats NITI 80% Target</div></div>', unsafe_allow_html=True)

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
            color_discrete_sequence=px.colors.qualitative.Dark24
        )
        fig_cat.update_layout(hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
        col_left.plotly_chart(fig_cat, use_container_width=True)
    
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
            color_discrete_sequence=["#EF4444", "#3B82F6", "#10B981", "#8B5CF6"]
        )
        fig_global.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
        col_right.plotly_chart(fig_global, use_container_width=True)
        
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
        col_chart.plotly_chart(fig_bar, use_container_width=True)
        
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
        col_scat.plotly_chart(fig_scat, use_container_width=True)
        
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
        st.plotly_chart(fig_ciar, use_container_width=True)

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
            st.metric("Total EVs", f"{int(row_a['ev_count']):,}", f"{int(row_b['ev_count']):,} ({state_b})")
        with m2:
            st.metric("EV Penetration %", f"{row_a['ev_penetration_pct']:.2f}%", f"{row_b['ev_penetration_pct']:.2f}%")
        with m3:
            st.metric("Public Chargers", f"{int(row_a['chargers']):,}", f"{int(row_b['chargers']):,}")
        with m4:
            st.metric("CIAR (EVs/Charger)", f"{row_a['ciar']:.1f}", f"{row_b['ciar']:.1f}")
        with m5:
            st.metric("3W Fleet Share %", f"{row_a['pct_3w']:.1f}%", f"{row_b['pct_3w']:.1f}%")
        with m6:
            st.metric("GSDP per Capita", f"₹{int(row_a['gsdp_pc_inr']):,}", f"₹{int(row_b['gsdp_pc_inr']):,}")
            
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
            color_discrete_sequence=["#2563EB", "#D97706"]
        )
        st.plotly_chart(fig_comp, use_container_width=True)
        
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
        st.plotly_chart(fig_cross, use_container_width=True)

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
            marker_color="#64748B"
        ))
        fig_bud.add_trace(go.Bar(
            x=df_policy["financial_year"],
            y=df_policy["fund_utilization_cr"],
            name="Fund Utilization (₹ Cr)",
            marker_color="#0D9488"
        ))
        fig_bud.add_trace(go.Scatter(
            x=df_policy["financial_year"],
            y=df_policy["utilization_pct"],
            name="Utilization Rate (%)",
            yaxis="y2",
            line=dict(color="#DC2626", width=3),
            mode="lines+markers"
        ))
        
        fig_bud.update_layout(
            title="Budget Allocation vs. Utilization & The 2023-24 Drop",
            yaxis=dict(title="Amount (₹ Crore)"),
            yaxis2=dict(title="Utilization Rate (%)", overlaying="y", side="right", range=[0, 115]),
            barmode="group",
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )
        col_bud.plotly_chart(fig_bud, use_container_width=True)
        
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
            col_eff.plotly_chart(fig_eff, use_container_width=True)
            
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
        st.plotly_chart(fig_proj, use_container_width=True)
        
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
