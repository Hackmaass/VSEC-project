"""
Unit Tests for Data Cleaning Pipeline
Project: Indian Air Quality and Weather Pattern Analysis Using Python
"""

import os
import pytest
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_AQ_PATH = os.path.join(BASE_DIR, "data", "raw", "air_quality_daily.csv")
RAW_W_PATH = os.path.join(BASE_DIR, "data", "raw", "weather_daily.csv")
RAW_C_PATH = os.path.join(BASE_DIR, "data", "raw", "cities.csv")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed", "india_air_quality_weather_merged.csv")

def test_raw_files_exist():
    """Verify that all raw source files exist and have non-zero size."""
    for path in [RAW_AQ_PATH, RAW_W_PATH, RAW_C_PATH]:
        assert os.path.exists(path), f"File missing: {path}"
        assert os.path.getsize(path) > 0, f"File empty: {path}"

def test_processed_dataset_exists():
    """Verify that cleaned and merged dataset exists."""
    assert os.path.exists(PROCESSED_PATH), f"Processed file missing: {PROCESSED_PATH}"
    assert os.path.getsize(PROCESSED_PATH) > 1000000, "Processed file smaller than expected"

def test_clean_dataset_shape_and_columns():
    """Verify cleaned dataset row count, column count, and required schema."""
    df = pd.read_csv(PROCESSED_PATH)
    assert len(df) == 77150, f"Expected 77,150 rows, got {len(df)}"
    assert df["city"].nunique() == 50, f"Expected 50 unique cities, got {df['city'].nunique()}"
    
    required_columns = [
        "date", "city", "pm2_5_mean", "pm10_mean", "no2_mean", "so2_mean",
        "o3_8h_max", "co_8h_max", "india_aqi", "india_aqi_category",
        "temperature_2m_mean", "relative_humidity_2m_mean", "wind_speed_10m_max",
        "precipitation_sum", "state", "region", "season", "year", "month"
    ]
    for col in required_columns:
        assert col in df.columns, f"Required column missing: {col}"

def test_missing_values_and_null_integrity():
    """Verify that there are zero unhandled nulls in key analytical fields."""
    df = pd.read_csv(PROCESSED_PATH)
    key_fields = ["date", "city", "pm2_5_mean", "pm10_mean", "india_aqi", 
                  "temperature_2m_mean", "relative_humidity_2m_mean", "region", "season"]
    for col in key_fields:
        null_count = df[col].isnull().sum()
        assert null_count == 0, f"Column {col} contains {null_count} unexpected null values"

def test_physical_range_constraints():
    """Verify physical feasibility of cleaned variables."""
    df = pd.read_csv(PROCESSED_PATH)
    
    # Pollutant concentrations cannot be negative
    assert (df["pm2_5_mean"] >= 0).all(), "Found negative PM2.5 concentration"
    assert (df["pm10_mean"] >= 0).all(), "Found negative PM10 concentration"
    assert (df["no2_mean"] >= 0).all(), "Found negative NO2 concentration"
    
    # Humidity must be strictly within [0, 100]%
    assert (df["relative_humidity_2m_mean"] >= 0).all(), "Found negative relative humidity"
    assert (df["relative_humidity_2m_mean"] <= 100).all(), "Found relative humidity > 100%"
    
    # Wind speed cannot be negative
    assert (df["wind_speed_10m_max"] >= 0).all(), "Found negative wind speed"
    
    # India AQI should be in standard CPCB scale (0 to 500)
    assert (df["india_aqi"] >= 0).all(), "Found negative AQI"
    assert (df["india_aqi"] <= 500).all(), "Found AQI above CPCB maximum scale of 500"

def test_temporal_features_validity():
    """Verify proper parsing of dates and seasons."""
    df = pd.read_csv(PROCESSED_PATH)
    df["date"] = pd.to_datetime(df["date"])
    
    assert df["date"].min() == pd.Timestamp("2022-08-05"), f"Unexpected start date: {df['date'].min()}"
    assert df["date"].max() == pd.Timestamp("2026-10-25"), f"Unexpected end date: {df['date'].max()}"
    
    valid_seasons = {"Winter", "Summer / Pre-Monsoon", "Monsoon", "Post-Monsoon"}
    actual_seasons = set(df["season"].unique())
    assert actual_seasons == valid_seasons, f"Unexpected seasons: {actual_seasons}"
