"""
British Airways Flight Delay Analysis - Data Cleaning Pipeline
Standardizes formats, cleans anomalies, removes duplicates, handles missing values,
preserves operationally meaningful negative delays, and logs comprehensive quality metrics.
"""

import os
import pandas as pd
import numpy as np

def clean_flight_data(df_raw, verbose=True):
    """
    Cleans raw flight operational data.
    
    Parameters:
    -----------
    df_raw : pd.DataFrame
        Raw flight operations dataframe.
    verbose : bool
        Whether to print cleaning audit logs.
        
    Returns:
    --------
    tuple: (pd.DataFrame, dict)
        Cleaned dataframe and data quality audit summary dictionary.
    """
    df = df_raw.copy()
    initial_rows = len(df)
    initial_cols = df.shape[1]
    
    audit = {
        'initial_rows': initial_rows,
        'initial_cols': initial_cols,
        'missing_values_before': df.isna().sum().to_dict(),
    }
    
    # 1. String Standardization & Trimming FIRST (so casing and whitespace differences are normalized for deduplication)
    string_cols = ['flight_number', 'airline', 'origin_airport', 'origin_city', 
                   'dest_airport', 'dest_city', 'tail_number', 'aircraft_type']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    if 'origin_airport' in df.columns:
        df['origin_airport'] = df['origin_airport'].str.upper()
    if 'dest_airport' in df.columns:
        df['dest_airport'] = df['dest_airport'].str.upper()
        
    # 2. Deduplication
    audit['duplicate_rows_detected'] = int(df.duplicated().sum())
    if verbose:
        print(f"--- DATA CLEANING PIPELINE STARTED ---")
        print(f"Initial Records: {initial_rows:,} | Initial Columns: {initial_cols}")
        print(f"Duplicate Rows Identified: {audit['duplicate_rows_detected']:,}")
        
    df = df.drop_duplicates().reset_index(drop=True)
    rows_after_dedup = len(df)
    audit['rows_after_dedup'] = rows_after_dedup
    audit['duplicates_removed'] = initial_rows - rows_after_dedup
    
    # 3. Datetime Parsing & Validation
    df['flight_date'] = pd.to_datetime(df['flight_date'], errors='coerce')
    df['scheduled_departure'] = pd.to_datetime(df['scheduled_departure'], errors='coerce')
    df['scheduled_arrival'] = pd.to_datetime(df['scheduled_arrival'], errors='coerce')
    df['actual_departure'] = pd.to_datetime(df['actual_departure'], errors='coerce')
    df['actual_arrival'] = pd.to_datetime(df['actual_arrival'], errors='coerce')
    
    # 4. Status Flags Formatting
    df['is_cancelled'] = df['is_cancelled'].fillna(0).astype(int)
    df['is_diverted'] = df['is_diverted'].fillna(0).astype(int)
    
    # Standardize cancellation reason
    df['cancellation_reason'] = df['cancellation_reason'].fillna('None').astype(str).str.strip()
    df.loc[df['is_cancelled'] == 0, 'cancellation_reason'] = 'None'
    
    # 5. Delay Causes Zero-Imputation
    delay_cause_cols = ['carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay']
    for col in delay_cause_cols:
        if col in df.columns:
            df.loc[df['is_cancelled'] == 0, col] = df.loc[df['is_cancelled'] == 0, col].fillna(0.0)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # 6. Negative Delay Preservation & Numeric Casting
    df['departure_delay'] = pd.to_numeric(df['departure_delay'], errors='coerce')
    df['arrival_delay'] = pd.to_numeric(df['arrival_delay'], errors='coerce')
    df['distance_km'] = pd.to_numeric(df['distance_km'], errors='coerce').astype(int)
    
    # 7. Duration Calculations (in minutes)
    df['scheduled_elapsed_time_min'] = (df['scheduled_arrival'] - df['scheduled_departure']).dt.total_seconds() / 60.0
    df['actual_elapsed_time_min'] = np.where(
        (df['is_cancelled'] == 0) & (df['actual_departure'].notna()) & (df['actual_arrival'].notna()),
        (df['actual_arrival'] - df['actual_departure']).dt.total_seconds() / 60.0,
        np.nan
    )
    
    # 8. Air Time vs Taxi/Holding Recovery Metrics
    df['delay_recovery_min'] = np.where(
        df['is_cancelled'] == 0,
        df['departure_delay'] - df['arrival_delay'],
        np.nan
    )
    
    audit['final_rows'] = len(df)
    audit['final_cols'] = df.shape[1]
    audit['missing_values_after'] = df.isna().sum().to_dict()
    audit['unique_airports'] = sorted(list(set(df['origin_airport'].unique()) | set(df['dest_airport'].unique())))
    audit['unique_aircraft'] = sorted(list(df['aircraft_type'].unique()))
    audit['date_range'] = (str(df['flight_date'].min().date()), str(df['flight_date'].max().date()))
    
    if verbose:
        print(f"Final Cleaned Records: {audit['final_rows']:,} | Final Columns: {audit['final_cols']}")
        print(f"Date Range: {audit['date_range'][0]} to {audit['date_range'][1]}")
        print(f"Unique Airports: {len(audit['unique_airports'])} | Unique Aircraft Types: {len(audit['unique_aircraft'])}")
        print(f"--- DATA CLEANING PIPELINE COMPLETED ---")
        
    return df, audit

def save_cleaned_data(df, output_path='data/processed/cleaned_flight_data.csv'):
    """Saves cleaned dataset to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved successfully to {output_path}")

if __name__ == '__main__':
    raw_path = 'data/raw/flight_data.csv'
    df_raw = pd.read_csv(raw_path)
    cleaned_df, audit_summary = clean_flight_data(df_raw, verbose=True)
    save_cleaned_data(cleaned_df)
