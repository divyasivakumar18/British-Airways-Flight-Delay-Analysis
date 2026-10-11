"""
Unit tests for data cleaning module.
"""
import pytest
import pandas as pd
import numpy as np
from src.data_cleaning import clean_flight_data

@pytest.fixture
def sample_raw_data():
    return pd.DataFrame({
        'flight_number': ['BA101', 'BA101', 'BA102', 'BA103'],
        'flight_date': ['2023-05-01', '2023-05-01', '2023-05-01', '2023-05-01'],
        'airline': [' British Airways ', 'British Airways', 'British Airways', 'British Airways'],
        'origin_airport': ['lhr', 'LHR', 'lgw', 'lhr'],
        'origin_city': ['London', 'London', 'London', 'London'],
        'dest_airport': ['jfk', 'JFK', 'ams', 'cdg'],
        'dest_city': ['New York', 'New York', 'Amsterdam', 'Paris'],
        'scheduled_departure': ['2023-05-01 10:00', '2023-05-01 10:00', '2023-05-01 12:00', '2023-05-01 14:00'],
        'actual_departure': ['2023-05-01 09:50', '2023-05-01 09:50', '2023-05-01 12:45', ''],
        'scheduled_arrival': ['2023-05-01 18:00', '2023-05-01 18:00', '2023-05-01 13:15', '2023-05-01 15:15'],
        'actual_arrival': ['2023-05-01 17:45', '2023-05-01 17:45', '2023-05-01 14:00', ''],
        'departure_delay': [-10.0, -10.0, 45.0, np.nan],
        'arrival_delay': [-15.0, -15.0, 45.0, np.nan],
        'distance_km': [5540, 5540, 358, 348],
        'tail_number': ['G-VIIA', 'G-VIIA', 'G-EUUA', 'G-EUUB'],
        'aircraft_type': ['B777-200ER', 'B777-200ER', 'A320-200', 'A320-200'],
        'is_cancelled': [0, 0, 0, 1],
        'cancellation_reason': [None, None, None, 'Weather'],
        'is_diverted': [0, 0, 0, 0],
        'carrier_delay': [np.nan, np.nan, 30.0, np.nan],
        'weather_delay': [np.nan, np.nan, 0.0, np.nan],
        'nas_delay': [np.nan, np.nan, 15.0, np.nan],
        'security_delay': [np.nan, np.nan, 0.0, np.nan],
        'late_aircraft_delay': [np.nan, np.nan, 0.0, np.nan]
    })

def test_deduplication(sample_raw_data):
    cleaned, audit = clean_flight_data(sample_raw_data, verbose=False)
    assert audit['duplicates_removed'] == 1
    assert len(cleaned) == 3

def test_negative_delays_preserved(sample_raw_data):
    cleaned, _ = clean_flight_data(sample_raw_data, verbose=False)
    early_flight = cleaned[cleaned['flight_number'] == 'BA101'].iloc[0]
    assert early_flight['departure_delay'] == -10.0
    assert early_flight['arrival_delay'] == -15.0

def test_cancellation_reasons(sample_raw_data):
    cleaned, _ = clean_flight_data(sample_raw_data, verbose=False)
    cancelled_flight = cleaned[cleaned['is_cancelled'] == 1].iloc[0]
    operated_flight = cleaned[cleaned['is_cancelled'] == 0].iloc[0]
    assert cancelled_flight['cancellation_reason'] == 'Weather'
    assert operated_flight['cancellation_reason'] == 'None'

def test_delay_cause_zero_imputation(sample_raw_data):
    cleaned, _ = clean_flight_data(sample_raw_data, verbose=False)
    early_flight = cleaned[cleaned['flight_number'] == 'BA101'].iloc[0]
    assert early_flight['carrier_delay'] == 0.0
    assert early_flight['weather_delay'] == 0.0
