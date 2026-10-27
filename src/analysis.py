"""
Numerical Statistical Analysis Module
Project: Indian Air Quality and Weather Pattern Analysis Using Python
Author: Academic Mini Project Developer

This module performs rigorous mathematical and statistical analysis using
NumPy and Pandas explicitly, providing clear explanations of every measure.
"""

import os
import json
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "india_air_quality_weather_merged.csv")
METRICS_DIR = os.path.join(BASE_DIR, "outputs", "metrics")
REPORTS_DIR = os.path.join(BASE_DIR, "outputs", "reports")

def calculate_variable_statistics(arr: np.ndarray, col_name: str) -> dict:
    """
    Computes statistical properties using NumPy functions explicitly.
    Includes Sample Mean, Median, Min, Max, Sample Variance, Sample Std Dev,
    and Key Percentiles (25th, 50th, 75th, 90th, 95th, 99th).
    """
    # Filter any NaNs or infinities if present
    valid_data = arr[np.isfinite(arr)]
    n = len(valid_data)
    
    if n == 0:
        return {"variable": col_name, "valid_observations": 0}

    # Explicit NumPy Computations
    mean_val = float(np.mean(valid_data))
    median_val = float(np.median(valid_data))
    min_val = float(np.min(valid_data))
    max_val = float(np.max(valid_data))
    
    # Sample variance uses ddof=1 (Bessel's correction for unbiased sample variance)
    var_val = float(np.var(valid_data, ddof=1))
    std_val = float(np.std(valid_data, ddof=1))
    
    # Percentiles
    p25, p50, p75, p90, p95, p99 = [
        float(x) for x in np.percentile(valid_data, [25, 50, 75, 90, 95, 99])
    ]
    iqr = p75 - p25

    return {
        "variable": col_name,
        "valid_observations": int(n),
        "mean": round(mean_val, 2),
        "median": round(median_val, 2),
        "minimum": round(min_val, 2),
        "maximum": round(max_val, 2),
        "sample_variance": round(var_val, 2),
        "sample_std_dev": round(std_val, 2),
        "iqr": round(iqr, 2),
        "percentile_25": round(p25, 2),
        "percentile_50": round(p50, 2),
        "percentile_75": round(p75, 2),
        "percentile_90": round(p90, 2),
        "percentile_95": round(p95, 2),
        "percentile_99": round(p99, 2)
    }

def run_numerical_analysis():
    """
    Executes full statistical analysis across all key pollutants and weather variables.
    Exports structured JSON and CSV reports.
    """
    print("=" * 70)
    print("RUNNING NUMERICAL & STATISTICAL ANALYSIS (NUMPY & PANDAS)")
    print("=" * 70)

    os.makedirs(METRICS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError(f"Cleaned dataset not found at {PROCESSED_DATA_PATH}. Run data_cleaning.py first.")

    df = pd.read_csv(PROCESSED_DATA_PATH)
    print(f"Loaded Cleaned Dataset: {len(df):,} records, {df.shape[1]} columns.\n")

    key_pollutants = [
        "pm2_5_mean", "pm10_mean", "no2_mean", "so2_mean", "o3_8h_max", "co_8h_max", "india_aqi"
    ]
    key_weather = [
        "temperature_2m_mean", "relative_humidity_2m_mean", "wind_speed_10m_max", "precipitation_sum"
    ]
    all_numerical = key_pollutants + key_weather

    # 1. Compute Univariate Statistical Metrics
    print("[1] Calculating Univariate Descriptive Statistics via NumPy...")
    stats_list = []
    for col in all_numerical:
        col_arr = df[col].to_numpy()
        stats = calculate_variable_statistics(col_arr, col)
        stats_list.append(stats)
        print(f"  * {col:25s} | Mean: {stats['mean']:8.2f} | Median: {stats['median']:8.2f} | Std: {stats['sample_std_dev']:8.2f} | P95: {stats['percentile_95']:8.2f}")

    df_stats_summary = pd.DataFrame(stats_list)
    stats_csv_path = os.path.join(REPORTS_DIR, "univariate_statistical_summary.csv")
    df_stats_summary.to_csv(stats_csv_path, index=False)
    print(f"  -> Exported to {stats_csv_path}")

    # 2. City-Wise Rankings: Top 10 Polluted vs Top 10 Cleanest
    print("\n[2] Computing City-Wise Pollution Rankings...")
    city_stats = df.groupby(["city", "state", "region"]).agg(
        observations=("date", "count"),
        pm2_5_mean=("pm2_5_mean", "mean"),
        pm2_5_median=("pm2_5_mean", "median"),
        pm10_mean=("pm10_mean", "mean"),
        india_aqi_mean=("india_aqi", "mean"),
        temp_mean=("temperature_2m_mean", "mean"),
        humidity_mean=("relative_humidity_2m_mean", "mean"),
        wind_mean=("wind_speed_10m_max", "mean")
    ).reset_index()

    city_stats["pm2_5_mean"] = city_stats["pm2_5_mean"].round(2)
    city_stats["pm10_mean"] = city_stats["pm10_mean"].round(2)
    city_stats["india_aqi_mean"] = city_stats["india_aqi_mean"].round(2)

    top_polluted_pm25 = city_stats.sort_values(by="pm2_5_mean", ascending=False).head(10).reset_index(drop=True)
    top_cleanest_pm25 = city_stats.sort_values(by="pm2_5_mean", ascending=True).head(10).reset_index(drop=True)

    city_ranking_path = os.path.join(REPORTS_DIR, "city_rankings.csv")
    city_stats.sort_values(by="pm2_5_mean", ascending=False).to_csv(city_ranking_path, index=False)
    print(f"  -> Exported City Rankings to {city_ranking_path}")

    # 3. Regional Analysis
    print("\n[3] Computing Regional Comparative Statistics...")
    regional_stats = df.groupby("region").agg(
        total_observations=("date", "count"),
        pm2_5_mean=("pm2_5_mean", "mean"),
        pm2_5_median=("pm2_5_mean", "median"),
        pm10_mean=("pm10_mean", "mean"),
        india_aqi_mean=("india_aqi", "mean"),
        temp_mean=("temperature_2m_mean", "mean"),
        humidity_mean=("relative_humidity_2m_mean", "mean"),
        wind_mean=("wind_speed_10m_max", "mean")
    ).round(2).reset_index()

    regional_csv_path = os.path.join(REPORTS_DIR, "regional_statistical_summary.csv")
    regional_stats.to_csv(regional_csv_path, index=False)
    print(f"  -> Exported Regional Summary to {regional_csv_path}")

    # 4. Seasonal Analysis
    print("\n[4] Computing Seasonal Comparative Statistics...")
    seasonal_stats = df.groupby("season").agg(
        total_observations=("date", "count"),
        pm2_5_mean=("pm2_5_mean", "mean"),
        pm2_5_median=("pm2_5_mean", "median"),
        pm2_5_std=("pm2_5_mean", "std"),
        pm10_mean=("pm10_mean", "mean"),
        india_aqi_mean=("india_aqi", "mean"),
        temp_mean=("temperature_2m_mean", "mean"),
        humidity_mean=("relative_humidity_2m_mean", "mean"),
        wind_mean=("wind_speed_10m_max", "mean"),
        precipitation_sum_mean=("precipitation_sum", "mean")
    ).round(2).reset_index()

    seasonal_csv_path = os.path.join(REPORTS_DIR, "seasonal_statistical_summary.csv")
    seasonal_stats.to_csv(seasonal_csv_path, index=False)
    print(f"  -> Exported Seasonal Summary to {seasonal_csv_path}")

    # 5. Correlation Analysis: Weather vs Air Quality
    print("\n[5] Computing Correlation Matrix (NumPy & Pandas)...")
    corr_vars = [
        "pm2_5_mean", "pm10_mean", "no2_mean", "so2_mean", "o3_8h_max", "co_8h_max", "india_aqi",
        "temperature_2m_mean", "relative_humidity_2m_mean", "wind_speed_10m_max", "precipitation_sum"
    ]
    corr_matrix = df[corr_vars].corr(method="pearson").round(3)
    corr_csv_path = os.path.join(REPORTS_DIR, "correlation_matrix.csv")
    corr_matrix.to_csv(corr_csv_path)
    print(f"  -> Exported Correlation Matrix to {corr_csv_path}")

    # Explicit NumPy Pearson correlation demonstration
    temp_arr = df["temperature_2m_mean"].to_numpy()
    pm25_arr = df["pm2_5_mean"].to_numpy()
    np_corr_temp_pm25 = float(np.corrcoef(temp_arr, pm25_arr)[0, 1])
    
    wind_arr = df["wind_speed_10m_max"].to_numpy()
    np_corr_wind_pm25 = float(np.corrcoef(wind_arr, pm25_arr)[0, 1])

    humidity_arr = df["relative_humidity_2m_mean"].to_numpy()
    np_corr_hum_pm25 = float(np.corrcoef(humidity_arr, pm25_arr)[0, 1])

    precip_arr = df["precipitation_sum"].to_numpy()
    np_corr_precip_pm25 = float(np.corrcoef(precip_arr, pm25_arr)[0, 1])

    print(f"  * NumPy Pearson r(Temperature, PM2.5):    {np_corr_temp_pm25:+.3f}")
    print(f"  * NumPy Pearson r(Wind Speed, PM2.5):     {np_corr_wind_pm25:+.3f}")
    print(f"  * NumPy Pearson r(Humidity, PM2.5):       {np_corr_hum_pm25:+.3f}")
    print(f"  * NumPy Pearson r(Precipitation, PM2.5):  {np_corr_precip_pm25:+.3f}")

    # 6. Compiling Full Statistical JSON
    full_metrics = {
        "dataset_metadata": {
            "total_records": int(len(df)),
            "cities_count": int(df["city"].nunique()),
            "states_count": int(df["state"].nunique()),
            "date_start": str(df["date"].min()),
            "date_end": str(df["date"].max())
        },
        "univariate_statistics": stats_list,
        "key_correlations_with_pm25": {
            "temperature_mean": round(np_corr_temp_pm25, 3),
            "wind_speed_max": round(np_corr_wind_pm25, 3),
            "relative_humidity_mean": round(np_corr_hum_pm25, 3),
            "precipitation_sum": round(np_corr_precip_pm25, 3)
        },
        "top_10_polluted_cities_pm25": top_polluted_pm25.to_dict(orient="records"),
        "top_10_cleanest_cities_pm25": top_cleanest_pm25.to_dict(orient="records"),
        "regional_breakdown": regional_stats.to_dict(orient="records"),
        "seasonal_breakdown": seasonal_stats.to_dict(orient="records")
    }

    summary_json_path = os.path.join(METRICS_DIR, "statistical_summary.json")
    with open(summary_json_path, "w") as f:
        json.dump(full_metrics, f, indent=2)

    print(f"\n[6] Full statistical summary exported to: {summary_json_path}")
    print("=" * 70)
    print("NUMERICAL ANALYSIS COMPLETE")
    print("=" * 70)

    return full_metrics

if __name__ == "__main__":
    run_numerical_analysis()
