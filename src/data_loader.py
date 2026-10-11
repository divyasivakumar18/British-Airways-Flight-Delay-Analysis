"""
British Airways Flight Delay Analysis - Data Generation and Loader Module
Generates a realistic, statistically grounded operational flight dataset
modeled on British Airways route network, UK/European CAA and US BTS delay dynamics.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Fix random seed for reproducible research
np.random.seed(42)
random.seed(42)

AIRPORTS = {
    # Hubs
    'LHR': {'city': 'London Heathrow', 'country': 'UK', 'type': 'Hub', 'lat': 51.4700, 'lon': -0.4543},
    'LGW': {'city': 'London Gatwick', 'country': 'UK', 'type': 'Hub', 'lat': 51.1537, 'lon': -0.1821},
    'LCY': {'city': 'London City', 'country': 'UK', 'type': 'Hub', 'lat': 51.5050, 'lon': 0.0553},
    # UK Domestic
    'EDI': {'city': 'Edinburgh', 'country': 'UK', 'type': 'Domestic', 'lat': 55.9500, 'lon': -3.3725},
    'GLA': {'city': 'Glasgow', 'country': 'UK', 'type': 'Domestic', 'lat': 55.8719, 'lon': -4.4331},
    'MAN': {'city': 'Manchester', 'country': 'UK', 'type': 'Domestic', 'lat': 53.3537, 'lon': -2.2750},
    'ABZ': {'city': 'Aberdeen', 'country': 'UK', 'type': 'Domestic', 'lat': 57.2019, 'lon': -2.1978},
    'BFS': {'city': 'Belfast Intl', 'country': 'UK', 'type': 'Domestic', 'lat': 54.6575, 'lon': -6.2158},
    'NCL': {'city': 'Newcastle', 'country': 'UK', 'type': 'Domestic', 'lat': 55.0375, 'lon': -1.6917},
    # European Short/Med Haul
    'CDG': {'city': 'Paris Charles de Gaulle', 'country': 'France', 'type': 'European', 'lat': 49.0097, 'lon': 2.5479},
    'AMS': {'city': 'Amsterdam Schiphol', 'country': 'Netherlands', 'type': 'European', 'lat': 52.3105, 'lon': 4.7683},
    'FRA': {'city': 'Frankfurt', 'country': 'Germany', 'type': 'European', 'lat': 50.0379, 'lon': 8.5622},
    'MAD': {'city': 'Madrid Barajas', 'country': 'Spain', 'type': 'European', 'lat': 40.4839, 'lon': -3.5680},
    'BCN': {'city': 'Barcelona El Prat', 'country': 'Spain', 'type': 'European', 'lat': 41.2974, 'lon': 2.0833},
    'FCO': {'city': 'Rome Fiumicino', 'country': 'Italy', 'type': 'European', 'lat': 41.8003, 'lon': 12.2389},
    'GVA': {'city': 'Geneva', 'country': 'Switzerland', 'type': 'European', 'lat': 46.2370, 'lon': 6.1092},
    'ZRH': {'city': 'Zurich', 'country': 'Switzerland', 'type': 'European', 'lat': 47.4582, 'lon': 8.5555},
    'DUB': {'city': 'Dublin', 'country': 'Ireland', 'type': 'European', 'lat': 53.4264, 'lon': -6.2499},
    'MUC': {'city': 'Munich', 'country': 'Germany', 'type': 'European', 'lat': 48.3537, 'lon': 11.7860},
    'ATH': {'city': 'Athens', 'country': 'Greece', 'type': 'European', 'lat': 37.9364, 'lon': 23.9484},
    'LIS': {'city': 'Lisbon', 'country': 'Portugal', 'type': 'European', 'lat': 38.7756, 'lon': -9.1354},
    'CPH': {'city': 'Copenhagen', 'country': 'Denmark', 'type': 'European', 'lat': 55.6180, 'lon': 12.6508},
    'VIE': {'city': 'Vienna', 'country': 'Austria', 'type': 'European', 'lat': 48.1103, 'lon': 16.5697},
    'NCE': {'city': 'Nice Cote d Azur', 'country': 'France', 'type': 'European', 'lat': 43.6653, 'lon': 7.2150},
    # Long-Haul Transatlantic and Americas
    'JFK': {'city': 'New York JFK', 'country': 'USA', 'type': 'Long-Haul', 'lat': 40.6413, 'lon': -73.7781},
    'BOS': {'city': 'Boston Logan', 'country': 'USA', 'type': 'Long-Haul', 'lat': 42.3656, 'lon': -71.0096},
    'ORD': {'city': 'Chicago O Hare', 'country': 'USA', 'type': 'Long-Haul', 'lat': 41.9742, 'lon': -87.9073},
    'LAX': {'city': 'Los Angeles', 'country': 'USA', 'type': 'Long-Haul', 'lat': 33.9416, 'lon': -118.4085},
    'SFO': {'city': 'San Francisco', 'country': 'USA', 'type': 'Long-Haul', 'lat': 37.6213, 'lon': -122.3790},
    'MIA': {'city': 'Miami', 'country': 'USA', 'type': 'Long-Haul', 'lat': 25.7959, 'lon': -80.2870},
    'IAD': {'city': 'Washington Dulles', 'country': 'USA', 'type': 'Long-Haul', 'lat': 38.9531, 'lon': -77.4565},
    'YYZ': {'city': 'Toronto Pearson', 'country': 'Canada', 'type': 'Long-Haul', 'lat': 43.6777, 'lon': -79.6248},
    'YVR': {'city': 'Vancouver', 'country': 'Canada', 'type': 'Long-Haul', 'lat': 49.1967, 'lon': -123.1815},
    # Long-Haul Middle East, Asia, Africa
    'DXB': {'city': 'Dubai Intl', 'country': 'UAE', 'type': 'Long-Haul', 'lat': 25.2532, 'lon': 55.3657},
    'DOH': {'city': 'Doha Hamad', 'country': 'Qatar', 'type': 'Long-Haul', 'lat': 25.2731, 'lon': 51.6081},
    'SIN': {'city': 'Singapore Changi', 'country': 'Singapore', 'type': 'Long-Haul', 'lat': 1.3644, 'lon': 103.9915},
    'HND': {'city': 'Tokyo Haneda', 'country': 'Japan', 'type': 'Long-Haul', 'lat': 35.5494, 'lon': 139.7798},
    'HKG': {'city': 'Hong Kong Intl', 'country': 'Hong Kong', 'type': 'Long-Haul', 'lat': 22.3080, 'lon': 113.9185},
    'DEL': {'city': 'Delhi Indira Gandhi', 'country': 'India', 'type': 'Long-Haul', 'lat': 28.5562, 'lon': 77.1000},
    'BOM': {'city': 'Mumbai Chhatrapati', 'country': 'India', 'type': 'Long-Haul', 'lat': 19.0896, 'lon': 72.8656},
    'JNB': {'city': 'Johannesburg OR Tambo', 'country': 'South Africa', 'type': 'Long-Haul', 'lat': -26.1367, 'lon': 28.2411},
    'CPT': {'city': 'Cape Town', 'country': 'South Africa', 'type': 'Long-Haul', 'lat': -33.9715, 'lon': 18.6021},
}

AIRCRAFT_FLEET = {
    'Short-Haul': [
        ('A319-100', ['G-EUPA', 'G-EUPB', 'G-EUPC', 'G-EUPD', 'G-EUPE'], 144),
        ('A320-200', ['G-EUUA', 'G-EUUB', 'G-EUUC', 'G-EUUD', 'G-EUUE'], 180),
        ('A320neo', ['G-TTNA', 'G-TTNB', 'G-TTNC', 'G-TTND', 'G-TTNE'], 180),
        ('A321neo', ['G-WNEA', 'G-WNEB', 'G-WNEC', 'G-WNED', 'G-WNEE'], 220),
        ('Embraer E190', ['G-LCYA', 'G-LCYB', 'G-LCYC', 'G-LCYD'], 98),
    ],
    'Long-Haul': [
        ('B777-200ER', ['G-VIIA', 'G-VIIB', 'G-VIIC', 'G-VIID', 'G-VIIE'], 272),
        ('B777-300ER', ['G-STBA', 'G-STBB', 'G-STBC', 'G-STBD'], 299),
        ('B787-8', ['G-ZBJA', 'G-ZBJB', 'G-ZBJC', 'G-ZBJD'], 214),
        ('B787-9', ['G-ZBKA', 'G-ZBKB', 'G-ZBKC', 'G-ZBKD'], 216),
        ('B787-10', ['G-ZBLA', 'G-ZBLB', 'G-ZBLC'], 256),
        ('A350-1000', ['G-XWBA', 'G-XWBB', 'G-XWBC', 'G-XWBD'], 331),
        ('A380-800', ['G-XLEA', 'G-XLEB', 'G-XLEC', 'G-XLED'], 469),
    ]
}

ROUTE_CONFIGS = [
    # LHR Domestic
    ('LHR', 'EDI', 8, 'Short-Haul', 'BA143', 534),
    ('LHR', 'GLA', 6, 'Short-Haul', 'BA147', 555),
    ('LHR', 'MAN', 6, 'Short-Haul', 'BA138', 243),
    ('LHR', 'ABZ', 4, 'Short-Haul', 'BA130', 647),
    ('LHR', 'BFS', 4, 'Short-Haul', 'BA141', 523),
    ('LHR', 'NCL', 4, 'Short-Haul', 'BA132', 404),
    # LHR European
    ('LHR', 'CDG', 8, 'Short-Haul', 'BA30', 348),
    ('LHR', 'AMS', 7, 'Short-Haul', 'BA42', 370),
    ('LHR', 'FRA', 6, 'Short-Haul', 'BA90', 655),
    ('LHR', 'MAD', 5, 'Short-Haul', 'BA45', 1246),
    ('LHR', 'BCN', 5, 'Short-Haul', 'BA47', 1148),
    ('LHR', 'FCO', 5, 'Short-Haul', 'BA54', 1445),
    ('LHR', 'GVA', 6, 'Short-Haul', 'BA72', 754),
    ('LHR', 'ZRH', 5, 'Short-Haul', 'BA71', 788),
    ('LHR', 'DUB', 6, 'Short-Haul', 'BA82', 449),
    ('LHR', 'MUC', 4, 'Short-Haul', 'BA95', 948),
    ('LHR', 'ATH', 3, 'Short-Haul', 'BA63', 2410),
    ('LHR', 'LIS', 4, 'Short-Haul', 'BA50', 1564),
    ('LHR', 'CPH', 4, 'Short-Haul', 'BA81', 980),
    ('LHR', 'VIE', 4, 'Short-Haul', 'BA69', 1275),
    ('LHR', 'NCE', 4, 'Short-Haul', 'BA34', 1032),
    # LHR Long-Haul
    ('LHR', 'JFK', 7, 'Long-Haul', 'BA11', 5540),
    ('LHR', 'BOS', 3, 'Long-Haul', 'BA21', 5245),
    ('LHR', 'ORD', 3, 'Long-Haul', 'BA29', 6360),
    ('LHR', 'LAX', 3, 'Long-Haul', 'BA26', 8780),
    ('LHR', 'SFO', 2, 'Long-Haul', 'BA28', 8630),
    ('LHR', 'MIA', 2, 'Long-Haul', 'BA20', 7135),
    ('LHR', 'IAD', 2, 'Long-Haul', 'BA21', 5910),
    ('LHR', 'YYZ', 2, 'Long-Haul', 'BA93', 5720),
    ('LHR', 'YVR', 2, 'Long-Haul', 'BA85', 7580),
    ('LHR', 'DXB', 3, 'Long-Haul', 'BA10', 5480),
    ('LHR', 'DOH', 2, 'Long-Haul', 'BA12', 5240),
    ('LHR', 'SIN', 2, 'Long-Haul', 'BA15', 10885),
    ('LHR', 'HND', 1, 'Long-Haul', 'BA05', 9590),
    ('LHR', 'HKG', 2, 'Long-Haul', 'BA31', 9640),
    ('LHR', 'DEL', 2, 'Long-Haul', 'BA14', 6710),
    ('LHR', 'BOM', 2, 'Long-Haul', 'BA13', 7200),
    ('LHR', 'JNB', 2, 'Long-Haul', 'BA55', 9070),
    ('LHR', 'CPT', 2, 'Long-Haul', 'BA59', 9680),
    # LGW Routes
    ('LGW', 'EDI', 3, 'Short-Haul', 'BA27', 566),
    ('LGW', 'GLA', 3, 'Short-Haul', 'BA28', 585),
    ('LGW', 'AMS', 3, 'Short-Haul', 'BA27', 358),
    ('LGW', 'BCN', 3, 'Short-Haul', 'BA26', 1110),
    ('LGW', 'FCO', 2, 'Short-Haul', 'BA25', 1409),
    ('LGW', 'NCE', 2, 'Short-Haul', 'BA26', 995),
    ('LGW', 'MIA', 1, 'Long-Haul', 'BA22', 7160),
    ('LGW', 'JFK', 1, 'Long-Haul', 'BA22', 5570),
    # LCY CityFlyer Routes
    ('LCY', 'EDI', 4, 'Short-Haul', 'BA87', 536),
    ('LCY', 'AMS', 4, 'Short-Haul', 'BA84', 335),
    ('LCY', 'FRA', 3, 'Short-Haul', 'BA87', 635),
    ('LCY', 'GVA', 3, 'Short-Haul', 'BA87', 742),
    ('LCY', 'ZRH', 3, 'Short-Haul', 'BA87', 768),
    ('LCY', 'DUB', 4, 'Short-Haul', 'BA84', 472),
]

def generate_flight_data(start_date='2023-01-01', end_date='2023-12-31'):
    """Generates realistic operational flight records for British Airways network."""
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    num_days = (end_dt - start_dt).days + 1
    
    records = []
    
    for day_idx in range(num_days):
        current_date = start_dt + timedelta(days=day_idx)
        month = current_date.month
        day_of_week = current_date.weekday()
        
        # Seasonality factors
        vol_multiplier = 1.0
        if month in [6, 7, 8]:
            vol_multiplier = 1.18
        elif month in [12]:
            vol_multiplier = 1.12
        elif month in [1, 2]:
            vol_multiplier = 0.88
            
        weather_risk = 0.08
        if month in [1, 2, 12]:
            weather_risk = 0.18
        elif month in [7, 8]:
            weather_risk = 0.13
            
        nas_risk = 0.10
        if month in [6, 7, 8, 9]:
            nas_risk = 0.22
        if day_of_week in [4, 6]:
            nas_risk += 0.05
            
        for origin, dest, daily_freq, haul, fn_prefix, distance in ROUTE_CONFIGS:
            for direction in ['Outbound', 'Inbound']:
                if direction == 'Outbound':
                    orig_code, dest_code = origin, dest
                else:
                    orig_code, dest_code = dest, origin
                    
                daily_count = max(1, int(round(daily_freq * vol_multiplier / 2.0)))
                
                if haul == 'Short-Haul':
                    if origin == 'LCY' or dest == 'LCY':
                        ac_model, tail_list, seats = AIRCRAFT_FLEET['Short-Haul'][4]
                    else:
                        ac_idx = np.random.choice([0, 1, 2, 3], p=[0.15, 0.40, 0.30, 0.15])
                        ac_model, tail_list, seats = AIRCRAFT_FLEET['Short-Haul'][ac_idx]
                else:
                    ac_idx = np.random.choice(range(len(AIRCRAFT_FLEET['Long-Haul'])), 
                                              p=[0.25, 0.20, 0.10, 0.20, 0.10, 0.10, 0.05])
                    ac_model, tail_list, seats = AIRCRAFT_FLEET['Long-Haul'][ac_idx]
                
                for f_idx in range(daily_count):
                    tail_num = np.random.choice(tail_list)
                    flight_num = f'{fn_prefix}{f_idx*2 + (1 if direction=="Outbound" else 2):02d}'
                    
                    if daily_count == 1:
                        dep_hour = np.random.choice([10, 13, 17, 19])
                    else:
                        hour_pool = np.linspace(6, 21, daily_count, endpoint=True)
                        dep_hour = int(hour_pool[f_idx])
                    dep_minute = np.random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
                    
                    sched_dep_dt = datetime(current_date.year, current_date.month, current_date.day, dep_hour, dep_minute)
                    sched_flight_minutes = int(round((distance / 780.0) * 60 + 35))
                    sched_arr_dt = sched_dep_dt + timedelta(minutes=sched_flight_minutes)
                    
                    cancel_prob = 0.015 + (weather_risk * 0.03) + (0.008 if haul == 'Short-Haul' else 0.003)
                    is_cancelled = 1 if np.random.rand() < cancel_prob else 0
                    
                    is_diverted = 0
                    cancellation_reason = None
                    if is_cancelled:
                        reasons = ['Weather', 'Carrier', 'Air Traffic System', 'Security']
                        probs = [0.45, 0.35, 0.18, 0.02] if weather_risk > 0.12 else [0.25, 0.50, 0.22, 0.03]
                        cancellation_reason = np.random.choice(reasons, p=probs)
                        dep_delay = np.nan
                        arr_delay = np.nan
                        actual_dep_str = ''
                        actual_arr_str = ''
                        carrier_delay = np.nan
                        weather_delay = np.nan
                        nas_delay = np.nan
                        security_delay = np.nan
                        late_aircraft_delay = np.nan
                    else:
                        if np.random.rand() < 0.002:
                            is_diverted = 1
                            
                        time_penalty = (dep_hour - 6) / 16.0 * 0.18
                        rand_draw = np.random.rand()
                        if rand_draw < 0.32:
                            # Early departure
                            dep_delay = int(-1 * np.random.exponential(scale=3.5))
                            dep_delay = max(-20, dep_delay)
                        elif rand_draw < 0.74:
                            # On time
                            dep_delay = int(np.random.uniform(0, 14))
                        else:
                            # Delayed (>15 mins)
                            mu = 3.3
                            sigma = 0.75
                            dep_delay = int(15 + np.random.lognormal(mean=mu, sigma=sigma))
                            dep_delay = min(720, dep_delay)
                            
                        air_adjustment = 0
                        if haul == 'Long-Haul' and dep_delay > 15:
                            air_adjustment -= int(np.random.uniform(5, 18))
                        if dest_code in ['LHR', 'LGW', 'AMS', 'JFK'] and np.random.rand() < 0.30:
                            air_adjustment += int(np.random.uniform(5, 25))
                            
                        arr_delay = dep_delay + air_adjustment + int(np.random.normal(0, 4))
                        arr_delay = max(-35, arr_delay)
                        
                        if is_diverted:
                            arr_delay = np.nan
                            
                        carrier_delay = 0.0
                        weather_delay = 0.0
                        nas_delay = 0.0
                        security_delay = 0.0
                        late_aircraft_delay = 0.0
                        
                        if arr_delay > 15 and not is_diverted:
                            tot_delay = float(arr_delay)
                            cause_weights = [0.28, weather_risk * 1.5, nas_risk * 1.4, 0.02, 0.32]
                            tot_w = sum(cause_weights)
                            cause_probs = [w / tot_w for w in cause_weights]
                            
                            primary_cause = np.random.choice(
                                ['Carrier', 'Weather', 'NAS', 'Security', 'Late Aircraft'],
                                p=cause_probs
                            )
                            
                            primary_pct = np.random.uniform(0.65, 1.0)
                            prim_mins = round(tot_delay * primary_pct, 1)
                            rem_mins = round(tot_delay - prim_mins, 1)
                            
                            if primary_cause == 'Carrier': carrier_delay = prim_mins
                            elif primary_cause == 'Weather': weather_delay = prim_mins
                            elif primary_cause == 'NAS': nas_delay = prim_mins
                            elif primary_cause == 'Security': security_delay = prim_mins
                            elif primary_cause == 'Late Aircraft': late_aircraft_delay = prim_mins
                            
                            if rem_mins > 0:
                                sec_cause = 'Late Aircraft' if primary_cause != 'Late Aircraft' else 'Carrier'
                                if sec_cause == 'Late Aircraft': late_aircraft_delay += rem_mins
                                else: carrier_delay += rem_mins
                        
                        act_dep_dt = sched_dep_dt + timedelta(minutes=dep_delay)
                        actual_dep_str = act_dep_dt.strftime('%Y-%m-%d %H:%M')
                        
                        if is_diverted:
                            actual_arr_str = ''
                        else:
                            act_arr_dt = sched_arr_dt + timedelta(minutes=arr_delay)
                            actual_arr_str = act_arr_dt.strftime('%Y-%m-%d %H:%M')
                            
                    records.append({
                        'flight_number': flight_num,
                        'flight_date': current_date.strftime('%Y-%m-%d'),
                        'airline': 'British Airways',
                        'origin_airport': orig_code,
                        'origin_city': AIRPORTS[orig_code]['city'],
                        'dest_airport': dest_code,
                        'dest_city': AIRPORTS[dest_code]['city'],
                        'scheduled_departure': sched_dep_dt.strftime('%Y-%m-%d %H:%M'),
                        'actual_departure': actual_dep_str,
                        'scheduled_arrival': sched_arr_dt.strftime('%Y-%m-%d %H:%M'),
                        'actual_arrival': actual_arr_str,
                        'departure_delay': dep_delay,
                        'arrival_delay': arr_delay,
                        'distance_km': distance,
                        'tail_number': tail_num,
                        'aircraft_type': ac_model,
                        'is_cancelled': is_cancelled,
                        'cancellation_reason': cancellation_reason,
                        'is_diverted': is_diverted,
                        'carrier_delay': carrier_delay,
                        'weather_delay': weather_delay,
                        'nas_delay': nas_delay,
                        'security_delay': security_delay,
                        'late_aircraft_delay': late_aircraft_delay,
                    })

    df = pd.DataFrame(records)
    
    # Introduce ~0.8% realistic duplicates for cleaning audit
    dup_sample = df.sample(frac=0.008, random_state=42)
    df_raw = pd.concat([df, dup_sample], ignore_index=True)
    df_raw = df_raw.sample(frac=1.0, random_state=42).reset_index(drop=True)
    return df_raw

def load_or_generate_raw_data(data_path='data/raw/flight_data.csv'):
    """Loads existing raw flight dataset or generates a new one if not present."""
    if os.path.exists(data_path):
        print(f"Loading raw dataset from {data_path}...")
        return pd.read_csv(data_path)
    else:
        print(f"Generating new raw operational flight dataset...")
        df = generate_flight_data()
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        df.to_csv(data_path, index=False)
        print(f"Saved {len(df):,} records to {data_path}")
        return df

if __name__ == '__main__':
    raw_df = load_or_generate_raw_data()
    print("Raw Data Summary:")
    print(f"Shape: {raw_df.shape}")
    print(f"Columns: {list(raw_df.columns)}")
    print(raw_df.head(3))
