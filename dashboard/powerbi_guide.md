# British Airways Flight Delay Analysis - Power BI Enterprise Dashboard Guide

This guide provides the complete Data Modeling blueprint, Star Schema relationships, DAX formulas, and page-by-page layout specification for recreating or extending the executive British Airways Operational Performance Dashboard in Microsoft Power BI Desktop.

---

## 1. Data Model & Architecture (Star Schema)

The analytical data model uses a standard dimensional Star Schema optimized for high-performance DAX aggregation and cross-filtering:

```text
               +-----------------------+
               |      DimCalendar      |
               +-----------------------+
               | Date (PK)             |
               | Year, Quarter, Month  |
               | DayOfWeek, Season     |
               +-----------+-----------+
                           | 1
                           |
                           | *
+-----------------------+  |  +-----------------------+
|      DimAirports      +--+--+      FactFlights      |
+-----------------------+  |  +-----------------------+
| AirportCode (PK)      |  |  | FlightID (PK)         |
| City, Country, Tier   |  |  | FlightNumber, TailNum |
| Latitude, Longitude   |  |  | DepDelay, ArrDelay    |
+-----------------------+  |  | DelayStatus, HaulType |
                           |  | Carrier/Late/NAS/Wx   |
                           |  +-----------+-----------+
+-----------------------+  |              | *
|       DimRoutes       +--+              |
+-----------------------+                 | 1
| RouteCode (PK)        |     +-----------+-----------+
| Origin, Destination   |     |    DimDelayCauses     |
| HaulType, Distance    |     +-----------------------+
| RiskScore, RiskTier   |     | CauseCategory (PK)    |
+-----------------------+     | Description           |
                              +-----------------------+
```

### Table Relationships:
- `DimCalendar[Date]` `1` <---> `*` `FactFlights[flight_date]`
- `DimAirports[AirportCode]` `1` <---> `*` `FactFlights[origin_airport]`
- `DimRoutes[route]` `1` <---> `*` `FactFlights[route]`

---

## 2. Key DAX Measures Library

Add these optimized DAX measures to your Power BI data model:

### A. Volume & Baseline Metrics
```dax
Total Scheduled Flights = COUNTROWS(FactFlights)

Operated Flights = 
CALCULATE(
    COUNTROWS(FactFlights),
    FactFlights[is_cancelled] = 0
)

Cancelled Flights = 
CALCULATE(
    COUNTROWS(FactFlights),
    FactFlights[is_cancelled] = 1
)

Delayed Flights = 
CALCULATE(
    COUNTROWS(FactFlights),
    FactFlights[is_cancelled] = 0,
    FactFlights[delay_status] = "Delayed"
)

On Time Flights = 
CALCULATE(
    COUNTROWS(FactFlights),
    FactFlights[is_cancelled] = 0,
    FactFlights[delay_status] = "On Time"
)
```

### B. Rates & Performance Indicators (KPIs)
```dax
Delay Rate % = 
DIVIDE([Delayed Flights], [Operated Flights], 0) * 100

On-Time Performance (OTP) % = 
DIVIDE([On Time Flights], [Operated Flights], 0) * 100

Cancellation Rate % = 
DIVIDE([Cancelled Flights], [Total Scheduled Flights], 0) * 100

Average Departure Delay (min) = 
CALCULATE(
    AVERAGE(FactFlights[departure_delay]),
    FactFlights[is_cancelled] = 0
)

Average Arrival Delay (min) = 
CALCULATE(
    AVERAGE(FactFlights[arrival_delay]),
    FactFlights[is_cancelled] = 0
)

Total Delay Minutes = 
CALCULATE(
    SUM(FactFlights[arrival_delay]),
    FactFlights[is_cancelled] = 0,
    FactFlights[arrival_delay] > 0
)
```

### C. Root Cause Pareto DAX Measures
```dax
Total Late Aircraft Delay Min = SUM(FactFlights[late_aircraft_delay])
Total Carrier Delay Min = SUM(FactFlights[carrier_delay])
Total NAS Air Traffic Delay Min = SUM(FactFlights[nas_delay])
Total Weather Delay Min = SUM(FactFlights[weather_delay])
Total Security Delay Min = SUM(FactFlights[security_delay])

Pareto Cumulative Delay % = 
VAR TotalAllDelays = CALCULATE([Total Delay Minutes], ALLSELECTED(FactFlights))
VAR CurrentDelay = [Total Delay Minutes]
RETURN
DIVIDE(
    CALCULATE(
        [Total Delay Minutes],
        FILTER(
            ALLSELECTED(DimDelayCauses),
            [Total Delay Minutes] >= CurrentDelay
        )
    ),
    TotalAllDelays,
    0
) * 100
```

### D. Scoring Models
```dax
Airport Operational Score = 
VAR OTP_Comp = [On-Time Performance (OTP) %] * 0.55
VAR Delay_Comp = MAX(0, 100 - ([Average Departure Delay (min)] * 2.5)) * 0.30
VAR Reliability_Comp = MAX(0, 100 - ([Cancellation Rate %] * 15.0)) * 0.15
RETURN
ROUND(OTP_Comp + Delay_Comp + Reliability_Comp, 1)

Airport Score Tier = 
SWITCH(
    TRUE(),
    [Airport Operational Score] >= 85, "Excellent",
    [Airport Operational Score] >= 70, "Good",
    [Airport Operational Score] >= 55, "Moderate",
    "Needs Improvement"
)
```

---

## 3. Power BI Multi-Page Report Layout

### Page 1 ? Executive Overview
- **Header:** British Airways Operational Command Center
- **KPI Card Row:** Total Flights, Delay Rate %, OTP %, Cancellation Rate %, Avg Delay (min), Total Delay Hours.
- **Visual 1 (Combo Chart):** Monthly Flight Volume (Bars) vs Delay Rate % (Line).
- **Visual 2 (Donut Chart):** Flight Status Distribution (On Time, Delayed, Cancelled, Diverted).
- **Visual 3 (Clustered Bar Chart):** Delay Severity Distribution (Early, 1-15 min, 16-30 min, 31-60 min, 61-120 min, 120+ min).
- **Visual 4 (Bar Chart):** Haul Type Performance Comparison.

### Page 2 ? Delay Root Cause & Pareto Analysis
- **Visual 1 (Pareto Chart):** Delay Cause (X-axis), Total Minutes (Column Y-axis), Cumulative % (Line Y-axis with 80% reference line).
- **Visual 2 (Matrix Table):** Delay Driver, Incident Count, Total Delay Minutes, Average Delay per Affected Flight.
- **Visual 3 (Scatter Plot):** Departure Delay vs Arrival Delay with Trendline (Slope = 0.96, showing in-flight recovery dynamics).

### Page 3 ? Airport Performance & Station Benchmarks
- **Visual 1 (Table with Data Bars):** Station IATA, City, Tier, Total Departures, Delay Rate %, Avg Dep Delay, OTP %, Airport Operational Score, Tier Badge.
- **Visual 2 (Scatter/Bubble Plot):** Station Volume (X-axis) vs Delay Rate % (Y-axis) sized by Avg Delay Minutes.
- **Visual 3 (Map Visual):** Geographic Airport locations colored by Performance Score.

### Page 4 ? Route Risk & Network Intelligence
- **Visual 1 (Bar Chart):** Top 15 Highest Risk Routes ranked by Composite Risk Index (Critical, High, Medium, Low).
- **Visual 2 (Matrix):** Route Pair, Haul Type, Distance (km), Scheduled Volume, Delay Rate %, Cancellation Rate %, Risk Tier.
- **Visual 3 (Scatter Plot):** Route Distance vs Average Arrival Delay.

### Page 5 ? Temporal Bottlenecks & Scheduling Heatmaps
- **Visual 1 (Matrix Heatmap with Conditional Formatting):** Day of Week (Rows) ? Departure Hour (Columns) with cell background colored by Delay Rate %.
- **Visual 2 (Line Chart):** Compounding Average Departure vs Arrival Delay across 24-hour day.
- **Visual 3 (Clustered Column Chart):** Seasonal Disruption Profile (Winter Fog vs Summer Air Traffic Constraints).

---

## 4. How to Import and Connect

1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV** -> Select `data/processed/flight_features.csv` (or click **Get Data** -> **SQLite Database** / **ODBC** and point to `data/processed/flight_analytics.db`).
3. Verify data types (`flight_date` as Date, delays as Decimal Numbers, codes as Text).
4. Paste the DAX measures from Section 2 into your model.
5. Apply British Airways corporate color palette:
   - Primary Blue: `#075AAA`
   - Crimson Accent: `#EB2226`
   - Dark Navy Background: `#0B162A`
   - Success Green: `#10B981`
   - Warning Amber: `#F59E0B`
