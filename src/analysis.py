"""
British Airways Flight Delay Analysis - Core Analytical Engine & Scoring Models
Computes business KPIs, Root Cause Pareto breakdown, Airport Performance Scores,
Route Risk Indexes, Delay Propagation regressions, and statistical tests.
"""

import os
import pandas as pd
import numpy as np
from scipy import stats

def compute_overall_kpis(df):
    """
    Computes top-level operational KPIs.
    """
    total_flights = len(df)
    operated_df = df[df['is_cancelled'] == 0]
    operated_flights = len(operated_df)
    cancelled_flights = int(df['is_cancelled'].sum())
    diverted_flights = int(df['is_diverted'].sum())
    
    delayed_flights = int((operated_df['delay_status'] == 'Delayed').sum())
    on_time_flights = int((operated_df['delay_status'] == 'On Time').sum())
    
    delay_rate_operated_pct = (delayed_flights / operated_flights * 100) if operated_flights > 0 else 0.0
    delay_rate_total_pct = (delayed_flights / total_flights * 100) if total_flights > 0 else 0.0
    cancellation_rate_pct = (cancelled_flights / total_flights * 100) if total_flights > 0 else 0.0
    otp_pct = (on_time_flights / operated_flights * 100) if operated_flights > 0 else 0.0
    
    valid_dep = operated_df['departure_delay'].dropna()
    valid_arr = operated_df['arrival_delay'].dropna()
    
    avg_dep_delay = float(valid_dep.mean())
    avg_arr_delay = float(valid_arr.mean())
    median_dep_delay = float(valid_dep.median())
    median_arr_delay = float(valid_arr.median())
    
    max_dep_delay = float(valid_dep.max())
    max_arr_delay = float(valid_arr.max())
    
    total_dep_delay_minutes = float(valid_dep[valid_dep > 0].sum())
    total_arr_delay_minutes = float(valid_arr[valid_arr > 0].sum())
    
    return {
        'total_flights': total_flights,
        'operated_flights': operated_flights,
        'cancelled_flights': cancelled_flights,
        'diverted_flights': diverted_flights,
        'delayed_flights': delayed_flights,
        'on_time_flights': on_time_flights,
        'delay_rate_operated_pct': round(delay_rate_operated_pct, 2),
        'delay_rate_total_pct': round(delay_rate_total_pct, 2),
        'cancellation_rate_pct': round(cancellation_rate_pct, 2),
        'on_time_performance_otp': round(otp_pct, 2),
        'avg_departure_delay_min': round(avg_dep_delay, 2),
        'avg_arrival_delay_min': round(avg_arr_delay, 2),
        'median_departure_delay_min': round(median_dep_delay, 2),
        'median_arrival_delay_min': round(median_arr_delay, 2),
        'max_departure_delay_min': round(max_dep_delay, 1),
        'max_arrival_delay_min': round(max_arr_delay, 1),
        'total_departure_delay_minutes': round(total_dep_delay_minutes, 1),
        'total_arrival_delay_minutes': round(total_arr_delay_minutes, 1),
    }

def compute_pareto_root_causes(df):
    """
    Performs Pareto (80/20) analysis on delay root causes.
    """
    op_df = df[df['is_cancelled'] == 0]
    
    cause_map = {
        'Late-Arriving Aircraft': 'late_aircraft_delay',
        'Carrier / Airline Operations': 'carrier_delay',
        'Air Traffic / NAS Flow': 'nas_delay',
        'Severe Weather': 'weather_delay',
        'Security Operations': 'security_delay'
    }
    
    records = []
    total_delay_minutes_all = sum(op_df[col].sum() for col in cause_map.values())
    
    for label, col in cause_map.items():
        total_mins = float(op_df[col].sum())
        incident_count = int((op_df[col] > 0).sum())
        pct_of_total = (total_mins / total_delay_minutes_all * 100) if total_delay_minutes_all > 0 else 0.0
        avg_per_incident = (total_mins / incident_count) if incident_count > 0 else 0.0
        
        records.append({
            'delay_cause': label,
            'delay_column': col,
            'total_delay_minutes': round(total_mins, 1),
            'incident_count': incident_count,
            'pct_of_total_minutes': round(pct_of_total, 2),
            'avg_delay_per_incident': round(avg_per_incident, 2)
        })
        
    pareto_df = pd.DataFrame(records).sort_values(by='total_delay_minutes', ascending=False).reset_index(drop=True)
    pareto_df['cumulative_delay_minutes'] = pareto_df['total_delay_minutes'].cumsum().round(1)
    pareto_df['cumulative_pct'] = (pareto_df['cumulative_delay_minutes'] / total_delay_minutes_all * 100).round(2)
    pareto_df['is_top_80_pct'] = pareto_df['cumulative_pct'] <= 85.0
    
    return pareto_df

def compute_airport_performance_score(df, min_flight_threshold=100):
    """
    Computes normalized Airport Operational Performance Score (0-100).
    Formula:
      Score = (OTP * 0.55) + (Delay_Score * 0.30) + (Reliability_Score * 0.15)
      Where Delay_Score = max(0, 100 - (Avg_Dep_Delay * 2.5))
            Reliability_Score = max(0, 100 - (Cancel_Rate * 15.0))
    """
    airport_stats = []
    
    for airport, group in df.groupby('origin_airport'):
        tot_fl = len(group)
        if tot_fl < min_flight_threshold:
            continue
            
        op_group = group[group['is_cancelled'] == 0]
        op_fl = len(op_group)
        canc_fl = int(group['is_cancelled'].sum())
        del_fl = int((op_group['delay_status'] == 'Delayed').sum())
        
        del_rate = (del_fl / op_fl * 100) if op_fl > 0 else 0.0
        canc_rate = (canc_fl / tot_fl * 100) if tot_fl > 0 else 0.0
        avg_dep_delay = float(op_group['departure_delay'].dropna().mean()) if op_fl > 0 else 0.0
        avg_arr_delay = float(op_group['arrival_delay'].dropna().mean()) if op_fl > 0 else 0.0
        otp_rate = ((op_fl - del_fl) / op_fl * 100) if op_fl > 0 else 0.0
        
        otp_component = otp_rate * 0.55
        delay_component = max(0.0, 100.0 - (max(0.0, avg_dep_delay) * 2.5)) * 0.30
        reliability_component = max(0.0, 100.0 - (canc_rate * 15.0)) * 0.15
        
        score = round(min(100.0, max(0.0, otp_component + delay_component + reliability_component)), 1)
        
        if score >= 85.0: tier = 'Excellent'
        elif score >= 70.0: tier = 'Good'
        elif score >= 55.0: tier = 'Moderate'
        else: tier = 'Needs Improvement'
        
        city = group['origin_city'].iloc[0]
        
        airport_stats.append({
            'airport_code': airport,
            'airport_city': city,
            'total_flights': tot_fl,
            'operated_flights': op_fl,
            'delayed_flights': del_fl,
            'delay_rate_pct': round(del_rate, 2),
            'cancellation_rate_pct': round(canc_rate, 2),
            'avg_departure_delay_min': round(avg_dep_delay, 2),
            'avg_arrival_delay_min': round(avg_arr_delay, 2),
            'on_time_performance_pct': round(otp_rate, 2),
            'performance_score': score,
            'performance_tier': tier
        })
        
    airport_df = pd.DataFrame(airport_stats).sort_values(by='performance_score', ascending=False).reset_index(drop=True)
    airport_df['rank'] = airport_df['performance_score'].rank(ascending=False, method='min').astype(int)
    return airport_df

def compute_route_risk_score(df, min_flight_threshold=50):
    """
    Computes Route Risk Index (0-100) and Category.
    """
    route_stats = []
    
    for route, group in df.groupby('route'):
        tot_fl = len(group)
        if tot_fl < min_flight_threshold:
            continue
            
        op_group = group[group['is_cancelled'] == 0]
        op_fl = len(op_group)
        canc_fl = int(group['is_cancelled'].sum())
        del_fl = int((op_group['delay_status'] == 'Delayed').sum())
        
        del_rate = (del_fl / op_fl * 100) if op_fl > 0 else 0.0
        canc_rate = (canc_fl / tot_fl * 100) if tot_fl > 0 else 0.0
        valid_arr = op_group['arrival_delay'].dropna()
        avg_arr_delay = float(valid_arr.mean()) if len(valid_arr) > 0 else 0.0
        p90_delay = float(valid_arr.quantile(0.90)) if len(valid_arr) > 0 else 0.0
        distance = int(group['distance_km'].iloc[0])
        haul = group['haul_type'].iloc[0]
        
        r_del = min(1.0, max(0.0, del_rate / 45.0)) * 35.0
        r_avg = min(1.0, max(0.0, avg_arr_delay / 35.0)) * 30.0
        r_canc = min(1.0, max(0.0, canc_rate / 5.0)) * 20.0
        r_p90 = min(1.0, max(0.0, p90_delay / 75.0)) * 15.0
        
        risk_score = round(min(100.0, max(0.0, r_del + r_avg + r_canc + r_p90)), 1)
        
        if risk_score >= 70.0: risk_cat = 'Critical'
        elif risk_score >= 50.0: risk_cat = 'High'
        elif risk_score >= 35.0: risk_cat = 'Medium'
        else: risk_cat = 'Low'
        
        route_stats.append({
            'route': route,
            'origin': group['origin_airport'].iloc[0],
            'destination': group['dest_airport'].iloc[0],
            'haul_type': haul,
            'distance_km': distance,
            'total_flights': tot_fl,
            'delayed_flights': del_fl,
            'delay_rate_pct': round(del_rate, 2),
            'cancellation_rate_pct': round(canc_rate, 2),
            'avg_arrival_delay_min': round(avg_arr_delay, 2),
            'p90_arrival_delay_min': round(p90_delay, 2),
            'risk_score': risk_score,
            'risk_category': risk_cat
        })
        
    route_df = pd.DataFrame(route_stats).sort_values(by='risk_score', ascending=False).reset_index(drop=True)
    return route_df

def compute_advanced_statistics(df):
    """
    Computes statistical tests, correlation matrices, and propagation regressions.
    """
    # Filter operated and non-diverted flights for clean arrival/departure pairings
    clean_pairs = df[(df['is_cancelled'] == 0) & (df['is_diverted'] == 0)].copy()
    clean_pairs = clean_pairs.dropna(subset=['departure_delay', 'arrival_delay'])
    
    # 1. Pearson & Spearman correlation between Departure and Arrival delays
    dep_arr_corr_pearson, p_pearson = stats.pearsonr(clean_pairs['departure_delay'], clean_pairs['arrival_delay'])
    dep_arr_corr_spearman, p_spearman = stats.spearmanr(clean_pairs['departure_delay'], clean_pairs['arrival_delay'])
    
    # 2. Linear Regression (Delay Propagation Slope)
    slope, intercept, r_val, p_val, std_err = stats.linregress(clean_pairs['departure_delay'], clean_pairs['arrival_delay'])
    
    # 3. Peak vs Off-Peak Two-Sample t-test
    peak_delays = clean_pairs[clean_pairs['is_peak_hour'] == 1]['arrival_delay']
    offpeak_delays = clean_pairs[clean_pairs['is_peak_hour'] == 0]['arrival_delay']
    t_stat, p_ttest = stats.ttest_ind(peak_delays, offpeak_delays, equal_var=False)
    
    # 4. Haul Type One-Way ANOVA
    short_delays = clean_pairs[clean_pairs['haul_type'] == 'Short-Haul']['arrival_delay']
    med_delays = clean_pairs[clean_pairs['haul_type'] == 'Medium-Haul']['arrival_delay']
    long_delays = clean_pairs[clean_pairs['haul_type'] == 'Long-Haul']['arrival_delay']
    f_stat, p_anova = stats.f_oneway(short_delays, med_delays, long_delays)
    
    return {
        'dep_arr_pearson_corr': round(dep_arr_corr_pearson, 4),
        'dep_arr_pearson_pvalue': float(p_pearson),
        'dep_arr_spearman_corr': round(dep_arr_corr_spearman, 4),
        'delay_propagation_slope': round(slope, 4),
        'delay_propagation_intercept': round(intercept, 4),
        'delay_propagation_r2': round(r_val**2, 4),
        'peak_vs_offpeak_tstat': round(t_stat, 4),
        'peak_vs_offpeak_pvalue': float(p_ttest),
        'peak_mean_arr_delay': round(float(peak_delays.mean()), 2),
        'offpeak_mean_arr_delay': round(float(offpeak_delays.mean()), 2),
        'haul_type_anova_fstat': round(f_stat, 4),
        'haul_type_anova_pvalue': float(p_anova),
        'short_haul_mean_arr_delay': round(float(short_delays.mean()), 2),
        'medium_haul_mean_arr_delay': round(float(med_delays.mean()), 2),
        'long_haul_mean_arr_delay': round(float(long_delays.mean()), 2),
    }

if __name__ == '__main__':
    df = pd.read_csv('data/processed/flight_features.csv')
    print("=== OVERALL KPIS ===")
    kpis = compute_overall_kpis(df)
    for k, v in kpis.items():
        print(f"{k}: {v}")
        
    print("\n=== ADVANCED STATISTICAL METRICS ===")
    stats_out = compute_advanced_statistics(df)
    for k, v in stats_out.items():
        print(f"{k}: {v}")
        
    print("\n=== AIRPORT PERFORMANCE (TOP 5) ===")
    airports = compute_airport_performance_score(df)
    print(airports[['rank', 'airport_code', 'airport_city', 'performance_score', 'performance_tier', 'delay_rate_pct']].head(5))
