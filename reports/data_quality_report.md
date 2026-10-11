# Data Quality and Hygiene Audit Report
**Project:** British Airways Flight Delay Analysis & Operational Performance System  
**Audit Date:** 2023 Full Operational Year Audit  
**Dataset Status:** Production Cleaned & Verified  

---

## 1. Executive Summary

This data quality audit evaluates the integrity, completeness, and consistency of the British Airways operational flight dataset. The dataset underwent comprehensive cleaning, deduplication, schema standardization, missing value handling, and operational validation.

| Metric | Raw Dataset | Processed Dataset | Variance / Action |
| :--- | :--- | :--- | :--- |
| **Total Records** | 75,681 | 75,080 | -601 duplicate rows removed |
| **Total Features / Columns** | 24 | 27 | +3 engineered duration/recovery features |
| **Date Span** | 2023-01-01 to 2023-12-31 | 2023-01-01 to 2023-12-31 | 365 days (Full Year coverage) |
| **Unique Airport Stations** | 42 | 42 | Standardized IATA 3-letter codes |
| **Unique Directed Routes** | 106 | 106 | Hub-and-spoke European & Long-Haul |
| **Cancelled Flights** | 1,915 (2.55%) | 1,915 (2.55%) | Missing actuals preserved as expected |
| **Diverted Flights** | 153 (0.20%) | 153 (0.20%) | Missing arrival delay flagged cleanly |

---

## 2. Missing Value Audit & Imputation Strategy

In aviation operational telemetry, missing values fall into two distinct business categories:
1. **Structural Missingness (Expected):** Cancelled flights do not have `actual_departure` or `actual_arrival` timestamps, nor do they record elapsed air times. Diverted flights do not record standard `actual_arrival` at the scheduled destination.
2. **Conditional Zeroes (Delay Causes):** Flights arriving on time or ahead of schedule do not generate delay sub-components (`carrier_delay`, `weather_delay`, `nas_delay`, `security_delay`, `late_aircraft_delay`). These are imputed to `0.0` minutes rather than dropped.

| Column Name | Raw Missing Count | Clean Missing Count | Clean Missing % |
| :--- | :--- | :--- | :--- |
| `flight_number` | 0 | 0 | 0.00% |
| `flight_date` | 0 | 0 | 0.00% |
| `airline` | 0 | 0 | 0.00% |
| `origin_airport` | 0 | 0 | 0.00% |
| `origin_city` | 0 | 0 | 0.00% |
| `dest_airport` | 0 | 0 | 0.00% |
| `dest_city` | 0 | 0 | 0.00% |
| `scheduled_departure` | 0 | 0 | 0.00% |
| `actual_departure` | 1,927 | 1,915 | 2.55% |
| `scheduled_arrival` | 0 | 0 | 0.00% |
| `actual_arrival` | 2,081 | 2,068 | 2.75% |
| `departure_delay` | 1,927 | 1,915 | 2.55% |
| `arrival_delay` | 2,081 | 2,068 | 2.75% |
| `distance_km` | 0 | 0 | 0.00% |
| `tail_number` | 0 | 0 | 0.00% |
| `aircraft_type` | 0 | 0 | 0.00% |
| `is_cancelled` | 0 | 0 | 0.00% |
| `cancellation_reason` | 73,754 | 73,165 | 97.45% |
| `is_diverted` | 0 | 0 | 0.00% |
| `carrier_delay` | 1,927 | 1,915 | 2.55% |
| `weather_delay` | 1,927 | 1,915 | 2.55% |
| `nas_delay` | 1,927 | 1,915 | 2.55% |
| `security_delay` | 1,927 | 1,915 | 2.55% |
| `late_aircraft_delay` | 1,927 | 1,915 | 2.55% |
| `scheduled_elapsed_time_min` | 0 | 0 | 0.00% |
| `actual_elapsed_time_min` | 0 | 2,068 | 2.75% |
| `delay_recovery_min` | 0 | 2,068 | 2.75% |

---

## 3. Anomaly Detection & Operational Integrity Checks

### A. Deduplication
- **Identified:** 601 exact duplicate flight transmission records.
- **Resolution:** Dropped duplicates while resetting DataFrame indexing to maintain key uniqueness.

### B. Negative Delay Preservation (Early Flights)
- **Early Departures:** 17,442 flights (23.84% of operated flights) departed between -20 and -1 minutes ahead of scheduled pushback.
- **Operational Validation:** Negative delays represent early turnaround and efficient ramp management. They are preserved intact as essential operational efficiency signals.

### C. Delay Duration Range & Outlier Audit
- **Departure Delay Range:** -20.0 min to 697.0 min (Mean: 15.01 min, Median: 6.0 min, 95th Percentile: 67.0 min).
- **Elapsed Duration Validation:** Verified that `actual_elapsed_time = actual_arrival - actual_departure` matches physical flight dynamics plus ground taxi times.

### D. Airport & Route Code Validation
- All origin and destination codes conform to standard 3-letter IATA identifiers.
- Verified 100% station coverage across UK Hubs (`LHR`, `LGW`, `LCY`), domestic destinations (`EDI`, `GLA`, `MAN`, `ABZ`, `BFS`, `NCL`), European capitals, and intercontinental long-haul gateways (`JFK`, `BOS`, `LAX`, `DXB`, `SIN`, `HND`, etc.).

---

## 4. Conclusion & Certification
The cleaned dataset (`cleaned_flight_data.csv`) satisfies all operational data governance standards for business analytics, SQL warehousing, predictive modeling, and executive dashboard integration.
