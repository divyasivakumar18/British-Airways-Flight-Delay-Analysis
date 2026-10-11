-- ==============================================================================
-- British Airways Flight Delay Analysis & Operational Performance SQL Suite
-- Database Engine: SQLite 3
-- Description: 12 Production-Grade Business Intelligence & Analytical Queries
-- ==============================================================================

-- ==============================================================================
-- QUERY 1: Top 10 Most Delayed Origin Airports
-- Identifies origin stations with highest delay rates and average departure delays
-- ==============================================================================
SELECT 
    f.origin_airport,
    a.city AS origin_city,
    a.airport_tier,
    COUNT(*) AS total_flights,
    SUM(CASE WHEN f.is_cancelled = 0 AND f.delay_status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_flights,
    ROUND(CAST(SUM(CASE WHEN f.is_cancelled = 0 AND f.delay_status = 'Delayed' THEN 1 ELSE 0 END) AS FLOAT) / 
          SUM(CASE WHEN f.is_cancelled = 0 THEN 1 ELSE 0 END) * 100, 2) AS delay_rate_pct,
    ROUND(AVG(CASE WHEN f.is_cancelled = 0 THEN f.departure_delay END), 2) AS avg_departure_delay_min,
    ROUND(AVG(CASE WHEN f.is_cancelled = 0 THEN f.arrival_delay END), 2) AS avg_arrival_delay_min,
    ROUND(CAST(SUM(f.is_cancelled) AS FLOAT) / COUNT(*) * 100, 2) AS cancellation_rate_pct
FROM flights f
LEFT JOIN airports a ON f.origin_airport = a.airport_code
GROUP BY f.origin_airport, a.city, a.airport_tier
HAVING COUNT(*) >= 100
ORDER BY delay_rate_pct DESC
LIMIT 10;


-- ==============================================================================
-- QUERY 2: Top 10 High-Risk Flight Routes Ranked by Risk Score and Cancellation Rate
-- Evaluates route vulnerability using the composite risk index
-- ==============================================================================
SELECT 
    r.route,
    r.haul_type,
    r.distance_km,
    r.total_flights,
    r.delayed_flights,
    r.delay_rate_pct,
    r.avg_arrival_delay_min,
    r.p90_arrival_delay_min,
    r.cancellation_rate_pct,
    r.risk_score,
    r.risk_category
FROM routes r
ORDER BY r.risk_score DESC
LIMIT 10;


-- ==============================================================================
-- QUERY 3: Monthly Operational KPI Trends
-- Tracks monthly volume, delay rate, on-time performance (OTP), and cancellations
-- ==============================================================================
WITH MonthlyAggregates AS (
    SELECT 
        year,
        month,
        month_name,
        season,
        COUNT(*) AS total_scheduled_flights,
        SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) AS operated_flights,
        SUM(is_cancelled) AS cancelled_flights,
        SUM(is_diverted) AS diverted_flights,
        SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_flights,
        SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'On Time' THEN 1 ELSE 0 END) AS on_time_flights,
        AVG(CASE WHEN is_cancelled = 0 THEN departure_delay END) AS avg_dep_delay,
        AVG(CASE WHEN is_cancelled = 0 THEN arrival_delay END) AS avg_arr_delay,
        SUM(CASE WHEN is_cancelled = 0 AND arrival_delay > 0 THEN arrival_delay ELSE 0 END) AS total_delay_minutes
    FROM flights
    GROUP BY year, month, month_name, season
)
SELECT 
    year,
    month,
    month_name,
    season,
    total_scheduled_flights,
    operated_flights,
    delayed_flights,
    ROUND(CAST(delayed_flights AS FLOAT) / operated_flights * 100, 2) AS delay_rate_pct,
    ROUND(CAST(on_time_flights AS FLOAT) / operated_flights * 100, 2) AS on_time_performance_otp_pct,
    ROUND(CAST(cancelled_flights AS FLOAT) / total_scheduled_flights * 100, 2) AS cancellation_rate_pct,
    ROUND(avg_dep_delay, 2) AS avg_dep_delay_min,
    ROUND(avg_arr_delay, 2) AS avg_arr_delay_min,
    ROUND(total_delay_minutes, 0) AS total_delay_minutes
FROM MonthlyAggregates
ORDER BY month ASC;


-- ==============================================================================
-- QUERY 4: Delay Root Cause Pareto Breakdown (80/20 Rule)
-- Calculates total delay minutes, percentage contribution, and cumulative share
-- ==============================================================================
SELECT 
    delay_cause,
    incident_count,
    total_delay_minutes,
    pct_of_total_minutes,
    cumulative_delay_minutes,
    cumulative_pct,
    avg_delay_per_incident,
    CASE WHEN is_top_80_pct = 1 THEN 'Yes (Vital Few)' ELSE 'No (Secondary Driver)' END AS is_pareto_vital_cause
FROM delay_root_causes
ORDER BY total_delay_minutes DESC;


-- ==============================================================================
-- QUERY 5: Day of Week Operational Disruption Analysis
-- Compares weekday vs weekend operational stability and turnaround delays
-- ==============================================================================
SELECT 
    day_of_week,
    day_name,
    is_weekend,
    COUNT(*) AS scheduled_flights,
    SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) AS operated_flights,
    SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_flights,
    ROUND(CAST(SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'Delayed' THEN 1 ELSE 0 END) AS FLOAT) / 
          SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) * 100, 2) AS delay_rate_pct,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN departure_delay END), 2) AS avg_dep_delay_min,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN arrival_delay END), 2) AS avg_arr_delay_min,
    ROUND(CAST(SUM(is_cancelled) AS FLOAT) / COUNT(*) * 100, 2) AS cancellation_rate_pct
FROM flights
GROUP BY day_of_week, day_name, is_weekend
ORDER BY day_of_week ASC;


-- ==============================================================================
-- QUERY 6: Hourly Flight Bank Congestion & Delay Propagation Analysis
-- Illustrates how delays compound throughout the operational day
-- ==============================================================================
SELECT 
    dep_hour,
    departure_time_category,
    is_peak_hour,
    COUNT(*) AS total_flights,
    SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_flights,
    ROUND(CAST(SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'Delayed' THEN 1 ELSE 0 END) AS FLOAT) / 
          SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) * 100, 2) AS delay_rate_pct,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN departure_delay END), 2) AS avg_departure_delay_min,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN arrival_delay END), 2) AS avg_arrival_delay_min,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN delay_recovery_min END), 2) AS avg_airborne_delay_recovery_min
FROM flights
GROUP BY dep_hour, departure_time_category, is_peak_hour
ORDER BY dep_hour ASC;


-- ==============================================================================
-- QUERY 7: Aircraft Fleet Reliability & Delay Propagation Analysis
-- Compares narrowbody vs widebody fleet operational efficiency
-- ==============================================================================
SELECT 
    aircraft_type,
    haul_type,
    COUNT(*) AS total_flights,
    SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) AS operated_flights,
    SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_flights,
    ROUND(CAST(SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'Delayed' THEN 1 ELSE 0 END) AS FLOAT) / 
          SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) * 100, 2) AS delay_rate_pct,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN departure_delay END), 2) AS avg_dep_delay_min,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN arrival_delay END), 2) AS avg_arr_delay_min,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN carrier_delay END), 2) AS avg_carrier_delay_min,
    ROUND(CAST(SUM(is_cancelled) AS FLOAT) / COUNT(*) * 100, 2) AS cancellation_rate_pct
FROM flights
GROUP BY aircraft_type, haul_type
ORDER BY total_flights DESC;


-- ==============================================================================
-- QUERY 8: Long-Haul vs Medium-Haul vs Short-Haul Operational Efficiency
-- Evaluates airborne recovery and OTP by haul category
-- ==============================================================================
SELECT 
    haul_type,
    COUNT(*) AS total_flights,
    SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) AS operated_flights,
    ROUND(CAST(SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'Delayed' THEN 1 ELSE 0 END) AS FLOAT) / 
          SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) * 100, 2) AS delay_rate_pct,
    ROUND(CAST(SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'On Time' THEN 1 ELSE 0 END) AS FLOAT) / 
          SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) * 100, 2) AS on_time_performance_otp,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN departure_delay END), 2) AS avg_dep_delay_min,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN arrival_delay END), 2) AS avg_arr_delay_min,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN delay_recovery_min END), 2) AS avg_delay_recovery_min,
    ROUND(CAST(SUM(is_cancelled) AS FLOAT) / COUNT(*) * 100, 2) AS cancellation_rate_pct
FROM flights
GROUP BY haul_type
ORDER BY total_flights DESC;


-- ==============================================================================
-- QUERY 9: Peak vs Off-Peak Flight Delay Disruption Benchmark
-- Quantifies congestion penalties during peak departure slots
-- ==============================================================================
SELECT 
    peak_period,
    COUNT(*) AS total_flights,
    SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) AS operated_flights,
    SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_flights,
    ROUND(CAST(SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'Delayed' THEN 1 ELSE 0 END) AS FLOAT) / 
          SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) * 100, 2) AS delay_rate_pct,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN departure_delay END), 2) AS avg_dep_delay_min,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN arrival_delay END), 2) AS avg_arr_delay_min,
    ROUND(CAST(SUM(is_cancelled) AS FLOAT) / COUNT(*) * 100, 2) AS cancellation_rate_pct
FROM flights
GROUP BY peak_period
ORDER BY total_flights DESC;


-- ==============================================================================
-- QUERY 10: Cancellation Root Causes and Seasonal Weather Impact
-- Analyzes primary drivers behind flight cancellations across seasons
-- ==============================================================================
SELECT 
    season,
    cancellation_reason,
    COUNT(*) AS cancellation_count,
    ROUND(CAST(COUNT(*) AS FLOAT) / SUM(COUNT(*)) OVER (PARTITION BY season) * 100, 2) AS pct_of_seasonal_cancellations
FROM flights
WHERE is_cancelled = 1
GROUP BY season, cancellation_reason
ORDER BY season, cancellation_count DESC;


-- ==============================================================================
-- QUERY 11: Top 10 Chronic Delayed Flight Numbers (BAxxxx)
-- Pinpoints specific scheduled flight numbers with recurrent major disruptions
-- ==============================================================================
SELECT 
    flight_number,
    route,
    aircraft_type,
    COUNT(*) AS flight_count,
    SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_occurrences,
    ROUND(CAST(SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'Delayed' THEN 1 ELSE 0 END) AS FLOAT) / 
          SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) * 100, 2) AS delay_rate_pct,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN arrival_delay END), 2) AS avg_arrival_delay_min,
    ROUND(MAX(CASE WHEN is_cancelled = 0 THEN arrival_delay END), 1) AS max_arrival_delay_min
FROM flights
GROUP BY flight_number, route, aircraft_type
HAVING COUNT(*) >= 150
ORDER BY delay_rate_pct DESC, avg_arrival_delay_min DESC
LIMIT 10;


-- ==============================================================================
-- QUERY 12: Route Performance Ranking within Haul Types (Window Functions)
-- Uses RANK() OVER (PARTITION BY haul_type) to rank routes within peer cohorts
-- ==============================================================================
WITH RouteAggregates AS (
    SELECT 
        route,
        origin_airport,
        dest_airport,
        haul_type,
        distance_km,
        COUNT(*) AS total_flights,
        SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) AS operated_flights,
        SUM(CASE WHEN is_cancelled = 0 AND delay_status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_flights,
        AVG(CASE WHEN is_cancelled = 0 THEN arrival_delay END) AS avg_arrival_delay
    FROM flights
    GROUP BY route, origin_airport, dest_airport, haul_type, distance_km
    HAVING COUNT(*) >= 50
)
SELECT 
    haul_type,
    route,
    total_flights,
    ROUND(CAST(delayed_flights AS FLOAT) / operated_flights * 100, 2) AS delay_rate_pct,
    ROUND(avg_arrival_delay, 2) AS avg_arrival_delay_min,
    RANK() OVER (PARTITION BY haul_type ORDER BY CAST(delayed_flights AS FLOAT) / operated_flights DESC) AS delay_rank_in_haul
FROM RouteAggregates
ORDER BY haul_type, delay_rank_in_haul ASC;
