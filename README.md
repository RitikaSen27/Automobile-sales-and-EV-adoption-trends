# Automobile Sales and EV Adoption Trends

A business analysis project studying electric vehicle (EV) adoption trends in India, using government data disclosed through Rajya Sabha (Parliament) session records.

## Project Goal

Analyze India's EV adoption journey end-to-end: registration growth over time, state-wise adoption patterns, charging infrastructure rollout, and the effectiveness of government incentive schemes (FAME-I, FAME-II, PM E-DRIVE) in driving that growth.

## Data Source

All 40 datasets in `datasets/` are sourced from **Rajya Sabha unstarred/starred question records** — official government responses to Parliament questions on the automobile and EV sector. Each filename follows the format `RS_Session_<session_no>_<AU/AS>_<question_no>.csv`.

## Repository Structure

```
├── datasets/                                    # Raw source CSVs (40 files, as published)
├── clean/                                        # Cleaned, theme-grouped master tables (generated, gitignored)
├── ev_cleaning.ipynb                             # Data cleaning & consolidation notebook (Python)
├── EV_Adoption_Project_Documentation.Rmd         # Key insights summary, by theme (R Markdown)
└── README.md
```

## Data Themes & Master Tables

The 40 raw files were grouped into 7 themes and consolidated into 29 cleaned master tables:

| Theme | Files | Description |
|---|---|---|
| EV Registration Trends | 7 | Year-over-year EV registration counts and % growth |
| State-wise EV Data | 7 | EV counts and adoption broken down by state/UT |
| Charging Infrastructure | 10 | Public charging station counts (state, highway, expressway) |
| Scheme Budget & Subsidy | 10 | FAME-I/II and PM E-DRIVE budget allocation vs. utilization |
| Sales by Vehicle Category | 3 | Sales/registration by 2W, 3W, 4W, commercial vehicles |
| Global Comparison | 1 | EV market share comparison across major regions |
| Manufacturer-specific | 2 | Data broken down by individual manufacturers |

## Methodology

1. **Inventory** — scanned all 40 raw files for shape, columns, and encoding issues before making structural assumptions
2. **Clean** — standardized column names, fixed typos, handled inconsistent representations of missing/approximate values (`NA`, `"approx."`, comma-formatted numbers)
3. **Consolidate** — grouped files by business theme and merged into master tables, reshaping wide-format files into long format where needed
4. **Verify** — checked for and removed hidden summary/total rows, and identified duplicate files (same underlying data published under different filenames) to avoid double-counting
5. **Document insights** — captured key findings per theme as they emerged, rather than after the fact

## Key Findings (Summary)

- India's EV adoption is **led by three-wheelers (especially e-rickshaws)**, not passenger cars — three-wheeler EV share rose from 14.4% (2018) to over 52% (2023), while passenger cars stayed under 2%.
- Adoption is **highly concentrated geographically** — a handful of states account for the vast majority of registrations and charging infrastructure.
- Government scheme **budget allocation has grown ~69x since 2015-16**, but fund utilization and subsidy uptake consistently lag allocation and targets, especially for 3-wheelers and 4-wheelers.
- India's growth mirrors a **global shift away from China-dominated EV markets**, with Europe emerging as the fastest-growing region.

Full theme-by-theme insights are documented in `EV_Adoption_Project_Documentation.Rmd`.

## Status

🚧 In progress — all 7 themes cleaned, consolidated, and documented. Next: exploratory data analysis, visualization, dashboard, and final report.
