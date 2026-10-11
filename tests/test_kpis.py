"""
Unit tests for KPI computations and score formulations.
"""
import pytest
import pandas as pd
from src.analysis import (
    compute_overall_kpis,
    compute_pareto_root_causes,
    compute_airport_performance_score,
    compute_route_risk_score,
    compute_advanced_statistics
)

@pytest.fixture
def feature_data():
    df = pd.read_csv('data/processed/flight_features.csv')
    return df

def test_kpi_consistency(feature_data):
    kpis = compute_overall_kpis(feature_data)
    assert kpis['total_flights'] == kpis['operated_flights'] + kpis['cancelled_flights']
    assert kpis['operated_flights'] == kpis['delayed_flights'] + kpis['on_time_flights'] + kpis['diverted_flights']
    assert round(kpis['delay_rate_operated_pct'] + kpis['on_time_performance_otp'], 1) >= 99.5

def test_pareto_integrity(feature_data):
    pareto = compute_pareto_root_causes(feature_data)
    assert len(pareto) == 5
    assert pareto['cumulative_pct'].iloc[-1] == 100.0
    assert pareto['total_delay_minutes'].is_monotonic_decreasing

def test_airport_score_bounds(feature_data):
    scores = compute_airport_performance_score(feature_data)
    assert (scores['performance_score'] >= 0.0).all()
    assert (scores['performance_score'] <= 100.0).all()
    assert scores['performance_tier'].isin(['Excellent', 'Good', 'Moderate', 'Needs Improvement']).all()

def test_route_risk_bounds(feature_data):
    routes = compute_route_risk_score(feature_data)
    assert (routes['risk_score'] >= 0.0).all()
    assert (routes['risk_score'] <= 100.0).all()
    assert routes['risk_category'].isin(['Critical', 'High', 'Medium', 'Low']).all()

def test_advanced_statistics(feature_data):
    stats = compute_advanced_statistics(feature_data)
    assert 0.0 <= stats['dep_arr_pearson_corr'] <= 1.0
    assert 0.0 <= stats['delay_propagation_r2'] <= 1.0
    assert stats['dep_arr_pearson_pvalue'] < 0.05
