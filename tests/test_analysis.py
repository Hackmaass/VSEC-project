"""
Unit Tests for Numerical and Statistical Analysis Module
Project: Indian Air Quality and Weather Pattern Analysis Using Python
"""

import os
import json
import pytest
import numpy as np
import pandas as pd
from src.analysis import calculate_variable_statistics

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed", "india_air_quality_weather_merged.csv")
STATS_JSON = os.path.join(BASE_DIR, "outputs", "metrics", "statistical_summary.json")
CITY_RANK_CSV = os.path.join(BASE_DIR, "outputs", "reports", "city_rankings.csv")

def test_numpy_statistical_calculation_accuracy():
    """Verify manual mathematical calculation against calculate_variable_statistics function."""
    sample_data = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    stats = calculate_variable_statistics(sample_data, "test_var")
    
    assert stats["valid_observations"] == 5
    assert stats["mean"] == 30.0
    assert stats["median"] == 30.0
    assert stats["minimum"] == 10.0
    assert stats["maximum"] == 50.0
    assert stats["sample_variance"] == 250.0  # (sum of squared deviations / (5-1))
    assert stats["sample_std_dev"] == round(np.sqrt(250.0), 2)
    assert stats["percentile_50"] == 30.0

def test_summary_metrics_file_validity():
    """Verify that statistical_summary.json exists and contains correct top-level keys."""
    assert os.path.exists(STATS_JSON), f"Metrics file missing: {STATS_JSON}"
    with open(STATS_JSON, "r") as f:
        data = json.load(f)
    
    required_keys = ["dataset_metadata", "univariate_statistics", "key_correlations_with_pm25", 
                     "top_10_polluted_cities_pm25", "top_10_cleanest_cities_pm25", "regional_breakdown", "seasonal_breakdown"]
    for k in required_keys:
        assert k in data, f"Missing key in statistical summary: {k}"

def test_meteorological_correlations_with_pm25():
    """Verify that expected meteorological correlations exist and fall within valid [-1, 1] range."""
    df = pd.read_csv(PROCESSED_PATH)
    
    r_wind = np.corrcoef(df["wind_speed_10m_max"], df["pm2_5_mean"])[0, 1]
    r_temp = np.corrcoef(df["temperature_2m_mean"], df["pm2_5_mean"])[0, 1]
    r_precip = np.corrcoef(df["precipitation_sum"], df["pm2_5_mean"])[0, 1]
    
    assert -1.0 <= r_wind <= 1.0
    assert -1.0 <= r_temp <= 1.0
    assert -1.0 <= r_precip <= 1.0
    
    # Wind speed should have a negative correlation with PM2.5 (ventilation and dispersion)
    assert r_wind < 0, f"Expected negative wind dispersion correlation, got {r_wind}"
    # Precipitation should have a negative correlation with PM2.5 (wet deposition)
    assert r_precip < 0, f"Expected negative precipitation scrubbing correlation, got {r_precip}"

def test_city_rankings_consistency():
    """Verify that city rankings CSV is present and properly sorted."""
    assert os.path.exists(CITY_RANK_CSV), f"City rankings CSV missing: {CITY_RANK_CSV}"
    df_rank = pd.read_csv(CITY_RANK_CSV)
    
    assert len(df_rank) == 50, f"Expected 50 ranked cities, got {len(df_rank)}"
    # Verify descending sort order by PM2.5 mean
    assert df_rank["pm2_5_mean"].is_monotonic_decreasing, "City rankings not sorted in descending order of PM2.5"
