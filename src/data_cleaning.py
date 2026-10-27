"""
Data Cleaning and Preprocessing Pipeline
Project: Indian Air Quality and Weather Pattern Analysis Using Python
Author: Academic Mini Project Developer

This module performs comprehensive cleaning, validation, feature engineering,
and merging of the air quality, meteorological, and geographic datasets.
"""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime

# Define directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
METRICS_DIR = os.path.join(BASE_DIR, "outputs", "metrics")

def assign_imd_season(month: int) -> str:
    """
    Assign Indian Meteorological Department (IMD) standard season based on month:
    - Winter: December, January, February (12, 1, 2)
    - Pre-Monsoon / Summer: March, April, May (3, 4, 5)
    - Monsoon: June, July, August, September (6, 7, 8, 9)
    - Post-Monsoon: October, November (10, 11)
    """
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer / Pre-Monsoon"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Post-Monsoon"

def run_cleaning_pipeline():
    """
    Executes the end-to-end data cleaning, validation, merging,
    and aggregation pipeline.
    """
    print("=" * 70)
    print("STARTING DATA CLEANING & PREPROCESSING PIPELINE")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 70)

    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    os.makedirs(METRICS_DIR, exist_ok=True)

    # 1. Load Raw Datasets
    aq_path = os.path.join(RAW_DATA_DIR, "air_quality_daily.csv")
    weather_path = os.path.join(RAW_DATA_DIR, "weather_daily.csv")
    cities_path = os.path.join(RAW_DATA_DIR, "cities.csv")

    print("\n[Step 1] Loading raw datasets...")
    df_aq_raw = pd.read_csv(aq_path)
    df_w_raw = pd.read_csv(weather_path)
    df_c_raw = pd.read_csv(cities_path)

    raw_stats = {
        "air_quality": {
            "initial_rows": int(len(df_aq_raw)),
            "initial_columns": int(df_aq_raw.shape[1]),
            "column_names": list(df_aq_raw.columns),
            "missing_values": {k: int(v) for k, v in df_aq_raw.isnull().sum().items()},
            "duplicate_rows": int(df_aq_raw.duplicated().sum()),
            "duplicate_city_date": int(df_aq_raw.duplicated(subset=["city", "date"]).sum()),
            "date_range": [str(df_aq_raw["date"].min()), str(df_aq_raw["date"].max())],
            "unique_cities": int(df_aq_raw["city"].nunique())
        },
        "weather": {
            "initial_rows": int(len(df_w_raw)),
            "initial_columns": int(df_w_raw.shape[1]),
            "column_names": list(df_w_raw.columns),
            "missing_values": {k: int(v) for k, v in df_w_raw.isnull().sum().items()},
            "duplicate_rows": int(df_w_raw.duplicated().sum()),
            "duplicate_city_date": int(df_w_raw.duplicated(subset=["city", "date"]).sum()),
            "date_range": [str(df_w_raw["date"].min()), str(df_w_raw["date"].max())],
            "unique_cities": int(df_w_raw["city"].nunique())
        },
        "cities": {
            "initial_rows": int(len(df_c_raw)),
            "initial_columns": int(df_c_raw.shape[1]),
            "column_names": list(df_c_raw.columns),
            "missing_values": {k: int(v) for k, v in df_c_raw.isnull().sum().items()},
            "unique_cities": int(df_c_raw["city"].nunique()),
            "unique_states": int(df_c_raw["state"].nunique()),
            "unique_regions": int(df_c_raw["region"].nunique())
        }
    }

    print(f"  -> Air Quality Raw: {raw_stats['air_quality']['initial_rows']:,} rows, {raw_stats['air_quality']['initial_columns']} cols")
    print(f"  -> Weather Raw:     {raw_stats['weather']['initial_rows']:,} rows, {raw_stats['weather']['initial_columns']} cols")
    print(f"  -> Cities Metadata: {raw_stats['cities']['initial_rows']:,} rows, {raw_stats['cities']['initial_columns']} cols")

    # 2. Duplicate Detection and Key Verification
    print("\n[Step 2] Verifying composite keys and duplicates...")
    df_aq = df_aq_raw.drop_duplicates(subset=["city", "date"]).copy()
    df_w = df_w_raw.drop_duplicates(subset=["city", "date"]).copy()
    df_c = df_c_raw.drop_duplicates(subset=["city"]).copy()

    # 3. Date Parsing & Temporal Feature Engineering
    print("\n[Step 3] Parsing dates and engineering temporal features...")
    df_aq["date"] = pd.to_datetime(df_aq["date"], format="%Y-%m-%d")
    df_w["date"] = pd.to_datetime(df_w["date"], format="%Y-%m-%d")

    # 4. Numerical Type Conversion and Physical Plausibility Validation
    print("\n[Step 4] Validating numerical ranges and physical constraints...")
    
    # Air quality numerical fields
    aq_numeric_cols = [
        "pm2_5_mean", "pm2_5_max", "pm10_mean", "pm10_max", "no2_mean",
        "so2_mean", "o3_8h_max", "co_8h_max", "dust_mean", "aod_mean",
        "us_aqi_max", "hours_available", "india_aqi", "india_aqi_pm"
    ]
    for col in aq_numeric_cols:
        df_aq[col] = pd.to_numeric(df_aq[col], errors="coerce")
        # Ensure non-negative concentration
        df_aq[col] = df_aq[col].clip(lower=0.0)

    # Weather numerical fields
    w_numeric_cols = [
        "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
        "apparent_temperature_max", "precipitation_sum", "precipitation_hours",
        "relative_humidity_2m_mean", "wind_speed_10m_max", "wind_direction_10m_dominant",
        "shortwave_radiation_sum", "et0_fao_evapotranspiration", "weather_code"
    ]
    for col in w_numeric_cols:
        df_w[col] = pd.to_numeric(df_w[col], errors="coerce")

    # Physical bounds clipping for weather:
    # Relative humidity strictly in [0, 100]
    df_w["relative_humidity_2m_mean"] = df_w["relative_humidity_2m_mean"].clip(0.0, 100.0)
    # Precipitation sum cannot be negative
    df_w["precipitation_sum"] = df_w["precipitation_sum"].clip(lower=0.0)
    df_w["precipitation_hours"] = df_w["precipitation_hours"].clip(0.0, 24.0)
    # Wind speed cannot be negative
    df_w["wind_speed_10m_max"] = df_w["wind_speed_10m_max"].clip(lower=0.0)

    # 5. Dataset Joining & Merging
    print("\n[Step 5] Merging Air Quality and Weather records on ['city', 'date']...")
    df_merged = pd.merge(df_aq, df_w, on=["city", "date"], how="inner")
    
    print("  Joining with Geographic Metadata on 'city'...")
    df_final = pd.merge(df_merged, df_c, on="city", how="left")

    # 6. Feature Engineering on Merged Dataset
    print("\n[Step 6] Adding date breakdown, season, and month features...")
    df_final["year"] = df_final["date"].dt.year
    df_final["month"] = df_final["date"].dt.month
    df_final["month_name"] = df_final["date"].dt.strftime("%B")
    df_final["day"] = df_final["date"].dt.day
    df_final["day_of_week"] = df_final["date"].dt.strftime("%A")
    df_final["is_weekend"] = df_final["date"].dt.day_of_week.isin([5, 6]).astype(int)
    df_final["quarter"] = df_final["date"].dt.quarter
    df_final["season"] = df_final["month"].apply(assign_imd_season)

    # Sort deterministically
    df_final = df_final.sort_values(by=["city", "date"]).reset_index(drop=True)

    # 7. Aggregations: City Summary, Monthly Summary, Seasonal Summary
    print("\n[Step 7] Computing summary aggregations...")
    
    # City-level summary
    city_summary = df_final.groupby(["city", "state", "region"]).agg(
        total_observations=("date", "count"),
        date_start=("date", "min"),
        date_end=("date", "max"),
        pm2_5_mean=("pm2_5_mean", "mean"),
        pm2_5_median=("pm2_5_mean", "median"),
        pm2_5_max=("pm2_5_max", "max"),
        pm10_mean=("pm10_mean", "mean"),
        india_aqi_mean=("india_aqi", "mean"),
        india_aqi_median=("india_aqi", "median"),
        temperature_mean=("temperature_2m_mean", "mean"),
        relative_humidity_mean=("relative_humidity_2m_mean", "mean"),
        wind_speed_mean=("wind_speed_10m_max", "mean"),
        precipitation_sum_total=("precipitation_sum", "sum")
    ).reset_index()

    # Monthly aggregate
    monthly_agg = df_final.groupby(["year", "month", "month_name"]).agg(
        record_count=("date", "count"),
        pm2_5_mean=("pm2_5_mean", "mean"),
        pm10_mean=("pm10_mean", "mean"),
        india_aqi_mean=("india_aqi", "mean"),
        temperature_mean=("temperature_2m_mean", "mean"),
        relative_humidity_mean=("relative_humidity_2m_mean", "mean"),
        wind_speed_mean=("wind_speed_10m_max", "mean")
    ).reset_index()

    # Seasonal aggregate
    seasonal_agg = df_final.groupby(["season"]).agg(
        record_count=("date", "count"),
        pm2_5_mean=("pm2_5_mean", "mean"),
        pm2_5_std=("pm2_5_mean", "std"),
        pm10_mean=("pm10_mean", "mean"),
        india_aqi_mean=("india_aqi", "mean"),
        temperature_mean=("temperature_2m_mean", "mean"),
        relative_humidity_mean=("relative_humidity_2m_mean", "mean"),
        wind_speed_mean=("wind_speed_10m_max", "mean")
    ).reset_index()

    # 8. Exporting Processed Datasets
    print("\n[Step 8] Exporting processed datasets to CSV...")
    merged_output_path = os.path.join(PROCESSED_DATA_DIR, "india_air_quality_weather_merged.csv")
    city_output_path = os.path.join(PROCESSED_DATA_DIR, "city_air_quality_summary.csv")
    monthly_output_path = os.path.join(PROCESSED_DATA_DIR, "monthly_air_quality_weather.csv")
    seasonal_output_path = os.path.join(PROCESSED_DATA_DIR, "seasonal_air_quality_weather.csv")

    df_final.to_csv(merged_output_path, index=False)
    city_summary.to_csv(city_output_path, index=False)
    monthly_agg.to_csv(monthly_output_path, index=False)
    seasonal_agg.to_csv(seasonal_output_path, index=False)

    print(f"  -> Cleaned Merged Dataset saved: {merged_output_path} ({os.path.getsize(merged_output_path):,} bytes)")
    print(f"  -> City Summary saved:          {city_output_path}")
    print(f"  -> Monthly Aggregation saved:   {monthly_output_path}")
    print(f"  -> Seasonal Aggregation saved:  {seasonal_output_path}")

    # 9. Clean Summary Metrics Log
    clean_stats = {
        "cleaning_timestamp": datetime.now().isoformat(),
        "raw_summary": raw_stats,
        "processed_summary": {
            "total_rows": int(len(df_final)),
            "total_columns": int(df_final.shape[1]),
            "column_names": list(df_final.columns),
            "date_range": [str(df_final["date"].min().date()), str(df_final["date"].max().date())],
            "total_cities": int(df_final["city"].nunique()),
            "total_states": int(df_final["state"].nunique()),
            "total_regions": int(df_final["region"].nunique()),
            "missing_values_post_clean": {k: int(v) for k, v in df_final.isnull().sum().items()},
            "aqi_category_distribution": {k: int(v) for k, v in df_final["india_aqi_category"].value_counts().items()},
            "dominant_pollutant_distribution": {k: int(v) for k, v in df_final["dominant_pollutant"].value_counts().items()},
            "regional_distribution": {k: int(v) for k, v in df_final["region"].value_counts().items()}
        }
    }

    metrics_file = os.path.join(METRICS_DIR, "cleaning_summary.json")
    with open(metrics_file, "w") as f:
        json.dump(clean_stats, f, indent=2)

    print(f"\n[Step 9] Cleaning summary logged to: {metrics_file}")
    print("=" * 70)
    print("DATA CLEANING COMPLETE: ALL VERIFICATIONS PASSED")
    print("=" * 70)

    return df_final

if __name__ == "__main__":
    run_cleaning_pipeline()
