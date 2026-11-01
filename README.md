# Automobile Sales and EV Adoption Trends

A comprehensive business analytics and strategy project analyzing electric vehicle (EV) adoption dynamics in India, built using official government data disclosed through Rajya Sabha (Parliament) session records, enriched with state socio-economic indicators and economic TCO modeling.

## Project Overview

This project studies India's EV adoption journey end-to-end:
- **Historical Trajectory:** Registration velocity, category adoption curves (2W, 3W, 4W, buses, freight).
- **Geographic Nuances:** State-level fleet penetration, charging station distribution, and per-capita metrics.
- **Total Cost of Ownership (TCO) Parity:** Comparative Capex + Opex modeling across 2W, 3W, and 4W (ICE vs. EV) revealing why commercial 3W adoption exploded while private 4W adoption stalled.
- **Policy Friction & Subsidy Efficiency:** Explaining the 2023–24 FAME-II budget utilization collapse (38.3% utilized) through Phased Manufacturing Programme (PMP) audits, OEM clawbacks, and subsidy cuts.
- **Charging Infrastructure Adequacy Ratio (CIAR):** Benchmarking state EV-to-charger ratios against the International Energy Agency (IEA) 10:1 standard.
- **Economic Hypothesis Testing:** Evaluating whether GSDP per capita and urbanization dictate adoption, or if vehicle utility rules (the "Wealth Paradox").
- **Machine Learning Segmentation:** K-Means clustering of 34 Indian states and UTs into actionable market archetypes.
- **Predictive Diffusion Modeling:** Logistic S-Curve (Bass Diffusion) forecasting category penetration through 2030 against NITI Aayog targets.
- **Strategic Advisory Framework:** Quantitative recommendations tailored for Automotive OEMs, Charging Point Operators (CPOs), and Policymakers.

## Data Sources

- **Primary Repository:** 40 raw datasets from **Rajya Sabha unstarred/starred question records** — official Ministry of Heavy Industries and Ministry of Road Transport & Highways disclosures. Each file follows the nomenclature `RS_Session_<session_no>_<AU/AS>_<question_no>.csv`.
- **Enrichment Datasets:** State population projections (MoHFW/Census of India), Per Capita Net State Domestic Product / GSDP at current prices (RBI / MoSPI State Finances), and Urbanization metrics.
- **Economic & TCO Benchmarks:** Automotive fuel/energy tariffs, vehicle purchase benchmarks (ARAI/OEM disclosures), and commercial operating mileage profiles.

## Repository Structure

```
├── datasets/                                    # Raw source CSVs (40 files, as published)
├── clean/                                       # Cleaned & enriched master tables (29 CSVs)
│   ├── state_ev_enriched.csv                    # 34-state master table (EVs, chargers, CIAR, pop, GSDP, clusters)
│   ├── ev_adoption_projections_2030.csv         # S-Curve adoption model forecasts (2018–2030) vs NITI targets
│   ├── tco_ice_vs_ev_comparison.csv             # 3-year & 5-year TCO, Opex/km, and payback periods across 2W, 3W, 4W
│   ├── subsidy_efficiency_analysis.csv          # FAME budget allocation, utilization %, and policy timeline shocks
│   └── ... (25 theme tables)
├── ev_cleaning.ipynb                            # Data audit, cleaning & consolidation notebook (Python)
├── ev_analysis.ipynb                            # Comprehensive analytics, predictive modeling & strategy notebook (Python)
├── EV_Adoption_Project_Documentation.Rmd        # Detailed analytical report and insights summary (R Markdown)
└── README.md
```

## Data Themes & Master Tables

The 40 raw source files and demographic/economic records were cleaned and consolidated into **29 master tables**:

| Theme | Files | Description |
|---|---|---|
| EV Registration Trends | 7 | Year-over-year EV registration counts and % growth |
| State-wise EV Data & Enrichment | 8 | EV counts, total vehicle fleet split, population, GSDP per capita, CIAR, and clusters |
| Charging Infrastructure | 10 | Public charging station counts (state, highway, expressway, OMC vs FAME) |
| Scheme Budget & Subsidy Efficiency | 12 | FAME-I/II and PM E-DRIVE budget allocation, utilization %, capital spend per vehicle, and target gaps |
| Sales by Vehicle Category | 3 | Sales and registration by 2W, 3W, 4W, commercial vehicles |
| Total Cost of Ownership (TCO) | 1 | Comparative Capex, running cost/km, 3/5-year TCO, and payback period across 2W, 3W, 4W |
| Global Comparison | 1 | Global EV market composition across China, Europe, USA, and Others |
| Manufacturer-specific | 2 | Registration breakdowns by vehicle class and transport category |
| Predictive Diffusion | 1 | 2018–2030 category adoption S-curves and NITI Aayog benchmarks |

## Analytical Structure (`ev_analysis.ipynb`)

The analysis is structured into three progressive analytical tiers:

### Part 1: Exploratory & Retrospective Analysis
- **Q1: How has EV registration grown over time?** Identifying the 2021 inflection point and clarifying reporting period mismatches (calendar vs. fiscal year).
- **Q2: Which vehicle categories are adopting EVs fastest?** Uncovering the 3-wheeler surge (14.4% in 2018 to >52% in 2023) vs. passenger cars (<2%).
- **Q3: Which states lead in EV adoption and charging infrastructure?** Identifying the stark mismatch between demand leader Uttar Pradesh and infrastructure leader Karnataka.
- **Q4: Is government subsidy funding keeping pace with targets?** Diagnosing the 2022–2024 budget utilization collapse (dropping to ~38% in FY24) and uneven vehicle subsidy uptake.
- **Q5: How does India's growth compare to global trends?** Contextualizing India's expansion alongside Europe's rapid rise and global diversification from China.

### Part 2: Advanced Analytics, Normalization & Predictive Modeling
- **Q6: How do states compare on normalized metrics?** Normalizing by total registered fleet and population. Demonstrating why absolute counts mislead: Assam (2.22%), Tripura (2.05%), Delhi (1.64%), and Bihar (1.37%) lead fleet electrification, while Delhi (1,095/100k) and Goa (788/100k) lead per capita.
- **Q7: What is the Charging Infrastructure Adequacy Ratio (CIAR) across states?** Calculating EVs per public charging station against the IEA 10:1 benchmark. Flagging acute deficits in Chandigarh (612:1), Bihar (464:1), Assam (436:1), and Uttar Pradesh (289:1, requiring ~55,500 additional chargers).
- **Q8: Does state wealth (GSDP per capita) drive EV adoption?** Revealing the "Wealth Paradox": GSDP per capita has essentially zero correlation with EV fleet penetration ($r = -0.010$), but strong correlation with public fast-charger density ($r = +0.605$). High income favors 2W and 4W purchases, while lower income favors commercial 3W e-rickshaws.
- **Q9: State Archetypes via K-Means Clustering:** Segmenting 34 states and UTs into 4 operational archetypes:
  1. *Commercial 3W Surge / Charger Deficit* (UP, Bihar, Assam, Tripura, Uttarakhand)
  2. *High-Income Infrastructure Pioneers* (Delhi, Karnataka, Goa)
  3. *Transition & Mixed Fleet Markets* (Rajasthan, Haryana, Chhattisgarh, Jharkhand, West Bengal, Chandigarh, Manipur)
  4. *Industrial & Personal EV Emerging* (Maharashtra, Gujarat, Tamil Nadu, Kerala, Punjab, etc.)
- **Q10: Technology Adoption S-Curve (Diffusion to 2030):** Fitting logistic diffusion curves against NITI Aayog targets:
  - **3W:** Projected to reach **88.2% by 2030** (exceeds the 80% target by 2026–2027).
  - **2W:** Projected to reach **71.8% by 2030** (strong growth, narrow 8% gap to the 80% target).
  - **4W:** Projected to reach **28.8% by 2030** (on-track to meet the 30% threshold right at 2030).
- **Q11: Total Cost of Ownership (TCO) Parity Framework:** Explaining the economics behind category divergence:
  - **Commercial 3W:** Payback in **3.7 months** due to high daily mileage (100–120 km) and ₹0.41/km vs. ₹3.40/km running cost arbitrage (generating >₹3.5 lakh net 3-year savings).
  - **Commuter 2W:** Payback in **20.7 months** (<2 years), supporting mass consumer transition.
  - **Passenger 4W:** Payback at **74.6 months (6.2 years)** due to high upfront battery premium (₹4.5 lakh) and lower daily mileage (30–35 km), exceeding typical car ownership turnover and freezing adoption.
- **Q12: Policy Friction & Capital Efficiency Analysis:** Explaining why FY24 budget utilization collapsed to 38.3%:
  - *The 3 Catalysts:* Phased Manufacturing Programme (PMP) audits freezing disbursements to 7 major OEMs, June 2023 subsidy reduction from ₹15k to ₹10k/kWh, and scheme expiration uncertainty.
  - *Capital Intensity Disparity:* e-2W achieved 79.3% of its target at ₹31,094 per vehicle; e-4W absorbed ₹167,838 per vehicle yet achieved only 12.4% of target; 1 e-bus consumed the subsidy budget of ~90 e-2-wheelers.

### Part 3: Actionable Strategic Recommendations (The "So What?" Framework)
Tailored strategic playbooks for:
1. **Automobile OEMs:** B2B commercial fleet prioritization, sub-₹12 lakh LFP battery hatchback focus, and Battery-as-a-Service (BaaS) swapping partnerships.
2. **Charging Point Operators (CPOs) & Energy Utilities:** Geographic capital reallocation toward high-deficit commercial corridors (UP, Bihar, Rajasthan) and off-peak Time-of-Use (TOU) tariffs.
3. **Policymakers (MHI / NITI Aayog / MoRTH):** Shifting PM E-DRIVE from capex subsidies to NBFC credit guarantees/interest subvention, and mandating state CIAR caps tied to infrastructure grants.

## Key Executive Insights

1. **India's EV Story is Commercial Livelihood First:** EV penetration is overwhelmingly led by commercial 3-wheelers (e-rickshaws) and delivery fleets where immediate operational fuel savings generate sub-4-month payback, independent of consumer subsidies.
2. **The 4W TCO Barrier:** Personal passenger cars require >6.2 years to recoup battery price premiums, explaining why private car EV share remains frozen under 2% without cheaper sub-₹12 lakh models.
3. **The Infrastructure-Demand Disconnect:** Public chargers are concentrated in wealthy tech hubs (Karnataka has 5,765 chargers for ~248k EVs), while the largest EV fleets operate in severe charger deserts (Uttar Pradesh has ~575k EVs but only 1,989 chargers).
4. **The Wealth Paradox:** State GSDP per capita does not predict EV fleet penetration ($r = -0.010$). Electric mobility in India is an economic equalizer driven by commercial utility rather than high-income luxury adoption.
5. **Subsidy Efficacy:** FAME-II's 2023-24 budget utilization collapsed to 38.3% due to localized component audit freezes and subsidy reductions, proving that regulatory stability and credit guarantees are more effective than upfront purchase hand-outs.
