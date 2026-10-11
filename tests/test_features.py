"""
Unit tests for feature engineering module.
"""
import pytest
import pandas as pd
import numpy as np
from src.feature_engineering import (
    categorize_delay_status,
    categorize_delay_severity,
    categorize_dep_time,
    categorize_haul,
    engineer_features
)

def test_delay_status_categorization():
    assert categorize_delay_status({'is_cancelled': 1, 'is_diverted': 0, 'arrival_delay': np.nan}) == 'Cancelled'
    assert categorize_delay_status({'is_cancelled': 0, 'is_diverted': 1, 'arrival_delay': np.nan}) == 'Diverted'
    assert categorize_delay_status({'is_cancelled': 0, 'is_diverted': 0, 'arrival_delay': 10.0}) == 'On Time'
    assert categorize_delay_status({'is_cancelled': 0, 'is_diverted': 0, 'arrival_delay': 15.0}) == 'On Time'
    assert categorize_delay_status({'is_cancelled': 0, 'is_diverted': 0, 'arrival_delay': 16.0}) == 'Delayed'
    assert categorize_delay_status({'is_cancelled': 0, 'is_diverted': 0, 'arrival_delay': -5.0}) == 'On Time'

def test_delay_severity_bins():
    assert categorize_delay_severity({'is_cancelled': 0, 'is_diverted': 0, 'arrival_delay': -10}) == 'Early / Ahead'
    assert categorize_delay_severity({'is_cancelled': 0, 'is_diverted': 0, 'arrival_delay': 12}) == 'On Time / Minor (1-15 min)'
    assert categorize_delay_severity({'is_cancelled': 0, 'is_diverted': 0, 'arrival_delay': 25}) == 'Short Delay (16-30 min)'
    assert categorize_delay_severity({'is_cancelled': 0, 'is_diverted': 0, 'arrival_delay': 45}) == 'Moderate Delay (31-60 min)'
    assert categorize_delay_severity({'is_cancelled': 0, 'is_diverted': 0, 'arrival_delay': 90}) == 'Major Delay (61-120 min)'
    assert categorize_delay_severity({'is_cancelled': 0, 'is_diverted': 0, 'arrival_delay': 150}) == 'Severe Delay (120+ min)'

def test_haul_type_bins():
    assert categorize_haul(500) == 'Short-Haul'
    assert categorize_haul(2500) == 'Medium-Haul'
    assert categorize_haul(6000) == 'Long-Haul'

def test_departure_time_bins():
    assert 'Early Morning' in categorize_dep_time(7)
    assert 'Morning' in categorize_dep_time(10)
    assert 'Afternoon' in categorize_dep_time(14)
    assert 'Evening' in categorize_dep_time(19)
    assert 'Night' in categorize_dep_time(23)
