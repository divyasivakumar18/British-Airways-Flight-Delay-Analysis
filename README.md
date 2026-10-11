# ?? British Airways Flight Delay Analysis & Operational Performance Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57.svg?logo=sqlite&logoColor=white)](https://sqlite.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com)
[![Power BI](https://img.shields.io/badge/Power_BI-Ready-F2C811.svg?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![Pytest](https://img.shields.io/badge/Pytest-15_Passed-0A9EDC.svg?logo=pytest&logoColor=white)](https://pytest.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade, portfolio-ready **Airline Operations & Business Intelligence System** analyzing flight delay dynamics, disruption root causes, airport performance scores, and route risk matrices across **75,000+ British Airways flights**.

---

## ?? Table of Contents
- [1. Business Problem & Project Overview](#1-business-problem--project-overview)
- [2. Technology Stack](#2-technology-stack)
- [3. End-to-End Architecture & Workflow](#3-end-to-end-architecture--workflow)
- [4. Project Repository Structure](#4-project-repository-structure)
- [5. Dataset Provenance & Quality Governance](#5-dataset-provenance--quality-governance)
- [6. Key Business KPIs & Empirical Findings](#6-key-business-kpis--empirical-findings)
- [7. Delay Root Cause & Pareto Analysis (80/20 Rule)](#7-delay-root-cause--pareto-analysis-8020-rule)
- [8. Airport Operational Performance Score (0?100)](#8-airport-operational-performance-score-0100)
- [9. Route Risk Assessment Matrix](#9-route-risk-assessment-matrix)
- [10. Advanced Statistical Analytics & Delay Propagation](#10-advanced-statistical-analytics--delay-propagation)
- [11. SQL Analytical Warehouse Suite](#11-sql-analytical-warehouse-suite)
- [12. Interactive BI Dashboard (Streamlit & Power BI)](#12-interactive-bi-dashboard-streamlit--power-bi)
- [13. Top 10 Actionable Business Insights](#13-top-10-actionable-business-insights)
- [14. Installation & Quickstart](#14-installation--quickstart)
- [15. Automated Testing Suite](#15-automated-testing-suite)
- [16. Future Roadmap](#16-future-roadmap)

---

## 1. Business Problem & Project Overview

Flight delays and irregular operations (IROPS) cost commercial airlines billions of dollars annually in fuel burn, ground handling penalties, crew flight time limitation (FTL) overruns, passenger hotel accommodation, and statutory **UK261 / EU261 passenger compensation claims** (?220??520 per affected customer).

### Core Objectives:
1. **Punctuality Telemetry:** Measure On-Time Performance (OTP) and delay severity across 75,000+ flights connecting London hubs (LHR, LGW, LCY) to 42 domestic and global spoke stations.
2. **Root Cause Attribution:** Decompose delays into **Carrier/Airline Ground Operations**, **Late-Arriving Aircraft (Turnaround Propagation)**, **Air Traffic Management (NAS)**, **Weather**, and **Security**.
3. **Compound Delay Dynamics:** Uncover how minor morning pushback delays cascade into major evening operational bottlenecks.
4. **Benchmarking & Risk Indexing:** Create normalized **Airport Performance Scores (0?100)** and **Route Risk Scores (0?100)** to pinpoint high-vulnerability network corridors.
5. **Interactive Business Intelligence:** Deploy an executive-level **5-Page Streamlit BI Web Dashboard** alongside a complete **Power BI Star Schema & DAX Modeling Guide**.

---

## 2. Technology Stack

| Domain | Tools & Libraries |
| :--- | :--- |
| **Programming & Data Science** | Python 3.10+, Pandas, NumPy, Scipy Stats |
| **Visual Analytics & Plotting** | Plotly Express & Graph Objects, Matplotlib, Seaborn |
| **Relational Database & SQL** | SQLite 3, SQLAlchemy, 12+ Complex CTE/Window SQL Queries |
| **Business Intelligence Portal** | Streamlit, Microsoft Power BI Desktop (Star Schema / DAX) |
| **Quality & Pipeline Testing** | Pytest, Nbformat, Nbconvert, Jupyter Lab |
| **Version Control & Docs** | Git, GitHub Markdown, Data Hygiene Audit Reports |

---

## 3. End-to-End Architecture & Workflow

```text
+-----------------------------------------------------------------------------------+
|                           1. RAW FLIGHT TELEMETRY                                 |
|      (75,681 Records | Hubs: LHR, LGW, LCY | European & Transatlantic Fleet)      |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                        2. DATA CLEANING & AUDITING PIPELINE                       |
|   ? Standardize IATA airport codes      ? Parse datetime stamps                   |
|   ? Remove duplicate transmissions      ? Preserve negative delays (early flights)|
|   ? Zero-impute delay causes for OTP    ? Calculate true duration & air recovery  |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                      3. FEATURE ENGINEERING & TAXONOMY                            |
|   ? Delay Status (On-Time, Delayed, Cancelled, Diverted) [Mutually Exclusive]     |
|   ? Severity Tiers (Early, 1-15 min, 16-30 min, 31-60 min, 61-120 min, 120+ min)  |
|   ? Temporal Bins (Season, Peak vs Off-Peak, 5-Bank Dep Periods, Weekday/Weekend) |
|   ? Haul Classification (Short-Haul <1500km, Medium 1500-4000km, Long >4000km)   |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                        4. ANALYTICS & SCORING ENGINES                             |
|   ? 80/20 Pareto Root Cause Decomposition                                         |
|   ? Normalized Airport Performance Score (0-100) & Operational Tiers              |
|   ? Route Risk Index (0-100) & Critical Category Tagging                          |
|   ? Delay Propagation Regression (Pearson r = 0.964, R? = 0.930)                  |
+------------------------------------------+----------------------------------------+
                                           |
                     +---------------------+---------------------+
                     |                                           |
                     v                                           v
+-----------------------------------------+ +---------------------------------------+
|        5. SQL ANALYTICS WAREHOUSE       | |       6. INTERACTIVE BI PORTAL        |
|  ? Ingested into SQLite Database        | |  ? 5-Page Streamlit App (app.py)      |
|  ? 12 Analytical Production SQL Queries | |  ? Power BI Star Schema & DAX Model   |
|  ? Multi-table indexing & aggregations  | |  ? Cross-filtering & Visual KPI cards |
+-----------------------------------------+ +---------------------------------------+
```

---

## 4. Project Repository Structure

```text
british-airways-flight-delay-analysis/
?
??? data/
?   ??? raw/
?   ?   ??? flight_data.csv             # 75,681 raw flight telemetry records
?   ??? processed/
?       ??? cleaned_flight_data.csv     # 75,080 deduplicated, cleansed records
?       ??? flight_features.csv         # 50 feature-engineered business attributes
?       ??? flight_analytics.db         # SQLite analytical relational database
?
??? notebooks/
?   ??? 01_data_cleaning.ipynb          # Step-by-step cleaning & audit logs
?   ??? 02_eda.ipynb                    # Multi-dimensional EDA & visualizations
?   ??? 03_business_analysis.ipynb      # Pareto, scoring models & SQL execution
?
??? src/
?   ??? __init__.py
?   ??? data_loader.py                  # Operational dataset generator & loader
?   ??? data_cleaning.py                # Robust cleaning pipeline
?   ??? feature_engineering.py          # Delay categories, time features & hauls
?   ??? analysis.py                     # KPI formulas, Pareto & scoring models
?   ??? database.py                     # SQLite engine & query runner
?
??? sql/
?   ??? flight_analysis.sql             # 12 production-grade SQL analytical queries
?
??? dashboard/
?   ??? app.py                          # 5-Page Interactive Streamlit BI Application
?   ??? powerbi_guide.md                # Power BI DAX library, Star Schema & layout
?
??? reports/
?   ??? data_quality_report.md          # Comprehensive data quality audit & hygiene
?   ??? insights.md                     # Top 10 data-driven insights & recommendations
?
??? tests/
?   ??? __init__.py
?   ??? test_cleaning.py                # Cleaning & negative delay preservation tests
?   ??? test_features.py                # Delay status & severity categorization tests
?   ??? test_kpis.py                    # KPI consistency & scoring range tests
?   ??? test_sql.py                     # SQLite schema & SQL query execution tests
?
??? requirements.txt                    # Exact production dependencies
??? README.md                           # Comprehensive portfolio documentation
??? .gitignore                          # Standard Python/IDE ignores
```

---

## 5. Dataset Provenance & Quality Governance

The operational dataset models British Airways' network structure spanning London Heathrow (LHR), London Gatwick (LGW), and London City (LCY) across 42 global stations over a full 365-day operational calendar.

### Key Data Hygiene Milestones (from [`reports/data_quality_report.md`](reports/data_quality_report.md)):
- **Raw Records Ingested:** 75,681 records across 24 columns.
- **Duplicate Telemetry Cleaned:** 601 exact duplicate transmission rows identified and purged.
- **Negative Delay Preservation:** 23,284 flights (31.82% of operated flights) departed between -20 and -1 minutes ahead of scheduled pushback. These were strictly preserved as crucial turnaround efficiency indicators.
- **Missing Value Handling:** Delay cause sub-components were cleanly zero-imputed (`0.0 min`) for on-time flights, preserving structural missingness for cancellations.

---

## 6. Key Business KPIs & Empirical Findings

Calculated over **75,080 processed scheduled flights** across calendar year 2023:

| Operational Metric | Formula / Definition | Value | Aviation Benchmark |
| :--- | :--- | :--- | :--- |
| **Total Scheduled Flights** | $\text{COUNT}(\text{All Flights})$ | **75,080** | 100.0% Network Volume |
| **Operated Flights** | $\text{COUNT}(\text{Cancelled} = 0)$ | **73,165** | 97.45% Completion Factor |
| **Cancelled Flights** | $\text{COUNT}(\text{Cancelled} = 1)$ | **1,915** | **2.55%** (Winter weather spike) |
| **Diverted Flights** | $\text{COUNT}(\text{Diverted} = 1)$ | **153** | **0.20%** |
| **Delayed Flights** | $\text{COUNT}(\text{ArrDelay} > 15 \text{ min})$ | **24,127** | **32.98%** of operated flights |
| **On-Time Performance (OTP)** | $\text{COUNT}(\text{ArrDelay} \le 15 \text{ min}) / \text{Operated}$ | **66.81%** | Target: > 75.0% |
| **Average Departure Delay** | $\text{AVG}(\text{Departure Delay})$ | **15.01 min** | Median: 6.0 min |
| **Average Arrival Delay** | $\text{AVG}(\text{Arrival Delay})$ | **16.48 min** | Median: 8.0 min |
| **Total Arrival Delay Hours** | $\sum(\text{Arrival Delay} > 0) / 60$ | **21,402 hrs** | 1,284,124 Total Minutes |
| **Severe Delays (>180 min)** | $\text{COUNT}(\text{ArrDelay} \ge 180 \text{ min})$ | **1,114 flights** | **1.52%** (UK261 liability) |

---

## 7. Delay Root Cause & Pareto Analysis (80/20 Rule)

Decomposing total delay minutes across all operated flights reveals a classic Pareto distribution:

```text
Rank  Delay Root Cause Driver       Total Delay Min   Share %    Cumulative %   Pareto Status
-----------------------------------------------------------------------------------------------
 1    Late-Arriving Aircraft        412,654 min       33.43%     33.43%         Vital Few (Top 80%)
 2    Carrier / Airline Operations  353,628 min       28.65%     62.08%         Vital Few (Top 80%)
 3    Air Traffic / NAS Flow        282,140 min       22.86%     84.94%         Vital Few (Top 80%)
 4    Severe Weather                161,289 min       13.07%     98.01%         Secondary Driver
 5    Security Operations            24,510 min        1.99%    100.00%         Secondary Driver
-----------------------------------------------------------------------------------------------
      TOTAL DELAY VOLUME          1,234,221 min      100.00%
```

> ?? **Key Finding:** **Late-Arriving Aircraft (33.4%)** and **Carrier Operations (28.7%)** generate **62.1% of all delay minutes**. Together with **NAS Air Traffic (22.9%)**, these top 3 causes account for **84.9% of total delay volume**.

---

## 8. Airport Operational Performance Score (0?100)

We developed a normalized composite scoring model evaluating station efficiency:

$$\text{Score} = (\text{OTP} \times 0.55) + \max(0, 100 - (\text{AvgDepDelay} \times 2.5)) \times 0.30 + \max(0, 100 - (\text{CancelRate} \times 15.0)) \times 0.15$$

### Classification Tiers:
- **90?100:** `Excellent` | **75?89:** `Good` | **60?74:** `Moderate` | **< 60:** `Needs Improvement`

### Station Benchmark Leaderboard Sample:
| Rank | Station | City / Region | Flights | Delay Rate | Avg Dep Delay | OTP % | Performance Score | Tier |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | `SFO` | San Francisco, USA | 722 | 31.1% | 14.1 min | 68.9% | **68.6** | Moderate |
| **2** | `LHR` | London Heathrow Hub | 37,215 | 27.7% | 12.8 min | 72.3% | **68.5** | Moderate |
| **3** | `BOM` | Mumbai, India | 727 | 33.9% | 14.8 min | 66.1% | **66.8** | Moderate |
| **4** | `LCY` | London City Hub | 4,213 | 29.2% | 13.9 min | 70.8% | **66.5** | Moderate |
| **5** | `LGW` | London Gatwick Hub | 6,942 | 29.6% | 14.3 min | 70.4% | **65.6** | Moderate |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
| **40**| `BFS` | Belfast Intl, UK | 1,460 | 40.6% | 18.0 min | 59.4% | **56.5** | Needs Improvement |
| **41**| `NCL` | Newcastle, UK | 1,444 | 40.3% | 18.5 min | 59.7% | **56.3** | Needs Improvement |
| **42**| `CPH` | Copenhagen, Denmark | 1,440 | 42.1% | 19.3 min | 57.9% | **54.9** | Needs Improvement |

---

## 9. Route Risk Assessment Matrix

The **Route Risk Index (0?100)** combines delay probability, average delay magnitude, 90th percentile delay severity ($P_{90}$), and cancellation frequency:

```text
Risk Score = (DelayRate / 45% * 35) + (AvgDelay / 35m * 30) + (CancelRate / 5% * 20) + (P90 / 75m * 15)
```

### High-Risk Scheduled Flight Corridors:
| Route Corridor | Haul Type | Distance | Volume | Delay Rate | Avg Arr Delay | $P_{90}$ Delay | Risk Score | Risk Tier |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `CPH -> LHR` | Short-Haul | 980 km | 1,440 | 42.1% | 20.9 min | 54.0 min | **75.1** | `Critical` |
| `NCL -> LHR` | Short-Haul | 404 km | 1,444 | 40.3% | 20.3 min | 51.0 min | **74.1** | `High` |
| `BFS -> LHR` | Short-Haul | 523 km | 1,460 | 40.6% | 19.9 min | 49.0 min | **73.1** | `High` |
| `EDI -> LGW` | Short-Haul | 566 km | 1,095 | 40.2% | 19.7 min | 50.0 min | **73.0** | `High` |
| `GLA -> LHR` | Short-Haul | 555 km | 2,176 | 40.2% | 19.8 min | 48.0 min | **72.5** | `High` |

---

## 10. Advanced Statistical Analytics & Delay Propagation

1. **Delay Propagation Linear Regression:**
   $$\text{Arrival Delay} = 0.9642 \times \text{Departure Delay} + 2.0063 \quad (R^2 = 0.9299, p < 10^{-100})$$
   - Pearson Correlation: $r = 0.9643$ | Spearman Rank Correlation: $\rho = 0.8703$.
   - A 10-minute departure delay translates into an average 11.6-minute arrival delay due to arrival holding stacks at LHR.
2. **Peak vs Off-Peak Two-Sample $t$-Test:**
   - Peak Hours (07:00?09:59 & 16:00?19:59) vs Off-Peak: $t = -3.7687, p = 0.00016$ (Statistically significant).
3. **Haul-Type One-Way ANOVA:**
   - Comparing Short-Haul (17.2 min mean), Medium-Haul (17.1 min mean), and Long-Haul (14.4 min mean):
   - $F = 72.8126, p = 2.57 \times 10^{-32}$ (Statistically significant in-flight speed recovery on transatlantic long-haul routes).

---

## 11. SQL Analytical Warehouse Suite

Located in [`sql/flight_analysis.sql`](sql/flight_analysis.sql), containing 12 production queries executed against `data/processed/flight_analytics.db`:
- **Query 1:** Top 10 Delayed Origin Airports (Delay Rate & Average Delay)
- **Query 2:** Top 10 High-Risk Routes by Composite Risk Score
- **Query 3:** Monthly Operational KPI Trend (Volume, OTP %, Cancellations)
- **Query 4:** Root Cause Pareto 80/20 Breakdown (Minutes & Cumulative %)
- **Query 5:** Day of Week Disruption Benchmark (Weekday vs Weekend)
- **Query 6:** Hourly Flight Bank Congestion & Propagation Curve
- **Query 7:** Fleet Aircraft Type Reliability (A320 vs B777 vs A350 vs A380)
- **Query 8:** Haul-Type Operational Efficiency Comparison
- **Query 9:** Peak vs Off-Peak Flight Delay Disruption Analysis
- **Query 10:** Cancellation Root Causes and Seasonal Weather Breakdown
- **Query 11:** Top 10 Chronic Delayed Flight Numbers (BAxxxx)
- **Query 12:** Route Performance Window Ranking (`RANK() OVER (PARTITION BY haul_type)`)

---

## 12. Interactive BI Dashboard (Streamlit & Power BI)

### Multi-Page Streamlit BI Web Application (`dashboard/app.py`):
- **Page 1 ? Executive Overview:** KPI cards with delta badges, monthly volume vs delay trend combo chart, status donut chart, and haul comparison.
- **Page 2 ? Delay Root Cause & Pareto:** Dual-axis 80/20 Pareto chart, cause impact matrix, and departure vs arrival delay scatter with OLS trendline.
- **Page 3 ? Airport Performance Scores:** Station ranking table with color bars, tier distribution donut, and station volume vs delay bubble plot.
- **Page 4 ? Route Risk Intelligence:** Top 15 risk routes horizontal bar chart, risk matrix table, and distance vs delay scatter.
- **Page 5 ? Temporal Bottlenecks & Scheduling:** Day of Week ? Departure Hour delay heatmap, compounding hourly delay curve, and seasonal weather profile.

### Power BI Enterprise Blueprint:
Detailed Star Schema relationships, DAX formulas, and canvas design specifications are documented in [`dashboard/powerbi_guide.md`](dashboard/powerbi_guide.md).

---

## 13. Top 10 Actionable Business Insights

Detailed findings and strategic recommendations from [`reports/insights.md`](reports/insights.md):

1. **Rotational Delay Compounding:** Late-arriving aircraft drive 33.4% of total delay minutes, cascading across 4?6 successive short-haul legs.  
   ?? *Recommendation:* Add 10 minutes of buffer ground time to afternoon narrowbody schedules at LHR/LGW.
2. **Diurnal Compounding Effect:** Delay rates escalate from **18.2% at 06:00** to **43.7% at 20:00** (+25.5 percentage points).  
   ?? *Recommendation:* Station dedicated "hot spare" A320 aircraft at LHR T5 from 16:00 to 21:00 to reset disrupted flight banks.
3. **Carrier Ground Handling Friction:** Internal ground operations generate 353,628 delay minutes (28.7% of total).  
   ?? *Recommendation:* Deploy IoT ramp milestone telemetry for baggage reconciliation and catering sign-off 15 min prior to SOBT.
4. **Air Traffic Slot Pressures:** European ATFM slot regulations account for 282,140 delay minutes, concentrated in summer months.  
   ?? *Recommendation:* Leverage pre-tactical CDM slot swapping to prioritize long-haul feeder sectors over domestic point-to-point legs.
5. **Transatlantic Delay Absorption:** Long-haul flights recover an average of 4.2 minutes in flight due to flexible cruise flight plans.  
   ?? *Recommendation:* Authorize dispatchers dynamic Cost-Index acceleration on transatlantic flights departing up to 30 min late.
6. **Friday & Sunday Peaks:** Friday (35.2% delay rate) and Sunday (34.8% delay rate) experience the highest disruption levels.  
   ?? *Recommendation:* Bolster ground handling and ramp workforce rosters by +20% during Friday/Sunday afternoon waves.
7. **Outstation Performance Variance:** European outstations (CPH, ATH, NCE) exhibit higher delay rates than primary hubs.  
   ?? *Recommendation:* Introduce contractual SLA punctuality bonuses and delay penalty clauses for third-party ground handlers.
8. **UK261 Compensation Exposure:** 1,114 flights (1.52%) suffered severe delays exceeding 180 minutes.  
   ?? *Recommendation:* Form an Operational Triage Protocol to prioritize flights approaching 90 minutes of ground delay.
9. **Seasonal Disruption Dichotomy:** Winter drives high cancellation rates (3.12%) via de-icing delays; Summer drives prolonged flight delays (36.1%).  
   ?? *Recommendation:* Expand de-icing pad capacity at LHR T5 remote stands and initiate proactive pre-cancellations 24h ahead of fog.
10. **Fleet Reliability Profile:** Narrowbody A320/A321 aircraft experience higher delay frequency (33.8%) than long-haul widebodies (29.1%).  
    ?? *Recommendation:* Integrate predictive maintenance telematics to swap high-failure avionics components during overnight checks.

---

## 14. Installation & Quickstart

### Prerequisites
- Python 3.10 or higher
- Git

### Setup Steps
```bash
# 1. Clone the repository
git clone https://github.com/username/british-airways-flight-delay-analysis.git
cd british-airways-flight-delay-analysis

# 2. Create and activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Run the end-to-end data pipeline
python src/data_loader.py
python src/data_cleaning.py
python src/feature_engineering.py
python src/analysis.py
python src/database.py

# 5. Launch the Interactive Streamlit BI Dashboard
streamlit run dashboard/app.py
```

---

## 15. Automated Testing Suite

Execute the full unit test suite covering data cleaning, feature bins, KPI consistency, scoring bounds, and SQLite queries:

```bash
pytest -v
```

### Test Coverage Results:
```text
tests/test_cleaning.py::test_deduplication PASSED                        [  6%]
tests/test_cleaning.py::test_negative_delays_preserved PASSED            [ 13%]
tests/test_cleaning.py::test_cancellation_reasons PASSED                 [ 20%]
tests/test_cleaning.py::test_delay_cause_zero_imputation PASSED          [ 26%]
tests/test_features.py::test_delay_status_categorization PASSED          [ 33%]
tests/test_features.py::test_delay_severity_bins PASSED                  [ 40%]
tests/test_features.py::test_haul_type_bins PASSED                       [ 46%]
tests/test_features.py::test_departure_time_bins PASSED                  [ 53%]
tests/test_kpis.py::test_kpi_consistency PASSED                          [ 60%]
tests/test_kpis.py::test_pareto_integrity PASSED                         [ 66%]
tests/test_kpis.py::test_airport_score_bounds PASSED                     [ 73%]
tests/test_kpis.py::test_route_risk_bounds PASSED                        [ 80%]
tests/test_kpis.py::test_advanced_statistics PASSED                      [ 86%]
tests/test_sql.py::test_database_tables_exist PASSED                     [ 93%]
tests/test_sql.py::test_sql_query_execution PASSED                       [100%]

============================= 15 passed in 6.77s ==============================
```

---

## 16. Future Roadmap

- [ ] **Live Flight Radar API Integration:** Stream live ADS-B telemetry and real-time airport slot updates.
- [ ] **Machine Learning Predictive Delay Models:** Train XGBoost / LightGBM models to predict flight delay probability 4 hours before scheduled off-blocks time.
- [ ] **Live METAR / TAF Weather Ingestion:** Incorporate runway visual range (RVR), crosswinds, and convective storm forecasts into route risk scores.
- [ ] **Aircraft Turnaround Simulation:** Build a discrete-event simulation (SimPy) to model gate turnaround bottlenecks and crew connection handoffs.

---

## ?? License
This project is open-source and licensed under the [MIT License](LICENSE).
