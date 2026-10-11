"""
British Airways Flight Delay Analysis - Feature Engineering Pipeline
Creates industry-standard aviation delay classifications, temporal dimensions,
flight haul definitions, peak indicators, and business metric features.
"""

import os
import pandas as pd
import numpy as np

def categorize_delay_status(row):
    """Assigns mutually exclusive delay status."""
    if row['is_cancelled'] == 1:
        return 'Cancelled'
    elif row['is_diverted'] == 1:
        return 'Diverted'
    elif pd.isna(row['arrival_delay']):
        return 'Unknown'
    elif row['arrival_delay'] > 15.0:
        return 'Delayed'
    else:
        return 'On Time'

def categorize_delay_severity(row):
    """Categorizes delay duration into business severity tiers."""
    if row['is_cancelled'] == 1:
        return 'Cancelled'
    elif row['is_diverted'] == 1:
        return 'Diverted'
    
    delay = row['arrival_delay']
    if pd.isna(delay):
        return 'Unknown'
    elif delay <= 0:
        return 'Early / Ahead'
    elif 1 <= delay <= 15:
        return 'On Time / Minor (1-15 min)'
    elif 16 <= delay <= 30:
        return 'Short Delay (16-30 min)'
    elif 31 <= delay <= 60:
        return 'Moderate Delay (31-60 min)'
    elif 61 <= delay <= 120:
        return 'Major Delay (61-120 min)'
    else:
        return 'Severe Delay (120+ min)'

def categorize_dep_time(hour):
    """Categorizes departure hour into operational flight bank time periods."""
    if 5 <= hour <= 8:
        return 'Early Morning (05:00-08:59)'
    elif 9 <= hour <= 11:
        return 'Morning (09:00-11:59)'
    elif 12 <= hour <= 16:
        return 'Afternoon (12:00-16:59)'
    elif 17 <= hour <= 21:
        return 'Evening (17:00-21:59)'
    else:
        return 'Night (22:00-04:59)'

def get_season(month):
    """Returns season based on UK meteorological definition."""
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

def categorize_haul(distance_km):
    """Categorizes route distance into flight haul types."""
    if distance_km < 1500:
        return 'Short-Haul'
    elif 1500 <= distance_km <= 4000:
        return 'Medium-Haul'
    else:
        return 'Long-Haul'

def engineer_features(df_clean, verbose=True):
    """
    Transforms cleaned flight dataframe with all business features.
    
    Parameters:
    -----------
    df_clean : pd.DataFrame
        Cleaned flight dataframe.
    verbose : bool
        Whether to print status logs.
        
    Returns:
    --------
    pd.DataFrame:
        Enriched dataframe with all engineered dimensions.
    """
    df = df_clean.copy()
    
    # 1. Parse datetime features
    df['flight_date'] = pd.to_datetime(df['flight_date'])
    df['scheduled_departure'] = pd.to_datetime(df['scheduled_departure'])
    df['scheduled_arrival'] = pd.to_datetime(df['scheduled_arrival'])
    
    # 2. Time Dimensions
    df['year'] = df['flight_date'].dt.year
    df['month'] = df['flight_date'].dt.month
    df['month_name'] = df['flight_date'].dt.strftime('%b')
    df['quarter'] = 'Q' + df['flight_date'].dt.quarter.astype(str)
    df['day_of_month'] = df['flight_date'].dt.day
    df['day_of_week'] = df['flight_date'].dt.dayofweek # 0=Mon, 6=Sun
    df['day_name'] = df['flight_date'].dt.strftime('%a')
    df['week_of_year'] = df['flight_date'].dt.isocalendar().week.astype(int)
    df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x in [5, 6] else 0)
    df['season'] = df['month'].apply(get_season)
    
    # 3. Departure Hour & Time Category
    df['dep_hour'] = df['scheduled_departure'].dt.hour
    df['departure_time_category'] = df['dep_hour'].apply(categorize_dep_time)
    
    # 4. Peak vs Off-Peak Hour
    # Peak slots: 07:00-09:59 and 16:00-19:59
    df['is_peak_hour'] = df['dep_hour'].apply(lambda h: 1 if h in [7, 8, 9, 16, 17, 18, 19] else 0)
    df['peak_period'] = df['is_peak_hour'].apply(lambda x: 'Peak' if x == 1 else 'Off-Peak')
    
    # 5. Route Dimensions
    df['route'] = df['origin_airport'] + ' -> ' + df['dest_airport']
    df['route_reverse'] = df['dest_airport'] + ' -> ' + df['origin_airport']
    df['route_pair'] = df.apply(lambda r: ' <-> '.join(sorted([r['origin_airport'], r['dest_airport']])), axis=1)
    df['haul_type'] = df['distance_km'].apply(categorize_haul)
    
    # 6. Delay Status & Categories
    df['delay_status'] = df.apply(categorize_delay_status, axis=1)
    df['delay_severity'] = df.apply(categorize_delay_severity, axis=1)
    
    # 7. Explicit Delay Minutes (standard aliases)
    df['departure_delay_minutes'] = df['departure_delay']
    df['arrival_delay_minutes'] = df['arrival_delay']
    
    # 8. Primary Delay Cause Identification (for operated delayed flights)
    def identify_primary_cause(row):
        if row['delay_status'] != 'Delayed':
            return 'None'
        causes = {
            'Late Aircraft': row.get('late_aircraft_delay', 0.0),
            'Carrier / Airline': row.get('carrier_delay', 0.0),
            'Air Traffic (NAS)': row.get('nas_delay', 0.0),
            'Weather': row.get('weather_delay', 0.0),
            'Security': row.get('security_delay', 0.0)
        }
        max_cause = max(causes.items(), key=lambda x: x[1])
        return max_cause[0] if max_cause[1] > 0 else 'Carrier / Airline'
        
    df['primary_delay_cause'] = df.apply(identify_primary_cause, axis=1)
    
    if verbose:
        print(f"--- FEATURE ENGINEERING COMPLETED ---")
        print(f"Total Rows: {len(df):,} | Total Columns: {df.shape[1]}")
        print("\nDelay Status Distribution:")
        print(df['delay_status'].value_counts(normalize=True).mul(100).round(2).to_string())
        print("\nHaul Type Distribution:")
        print(df['haul_type'].value_counts(normalize=True).mul(100).round(2).to_string())
        
    return df

def save_features(df, output_path='data/processed/flight_features.csv'):
    """Saves feature-engineered dataframe to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Feature dataset successfully saved to {output_path}")

if __name__ == '__main__':
    cleaned_path = 'data/processed/cleaned_flight_data.csv'
    df_clean = pd.read_csv(cleaned_path)
    df_features = engineer_features(df_clean, verbose=True)
    save_features(df_features)
