"""
Visualization Module
Project: Indian Air Quality and Weather Pattern Analysis Using Python
Author: Academic Mini Project Developer

This module generates publication-quality, high-resolution figures (300 DPI)
saved in outputs/figures/ using Matplotlib and Seaborn.
"""

import os
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless server execution
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "india_air_quality_weather_merged.csv")
FIGURES_DIR = os.path.join(BASE_DIR, "outputs", "figures")

# Configure publication aesthetics
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["axes.linewidth"] = 0.8

def generate_all_figures():
    """Generates all 5 mandatory figures + 1 regional/seasonal dynamics figure."""
    os.makedirs(FIGURES_DIR, exist_ok=True)
    
    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError(f"Cleaned dataset not found at {PROCESSED_DATA_PATH}")

    df = pd.read_csv(PROCESSED_DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])

    print("=" * 70)
    print("GENERATING HIGH-RESOLUTION PUBLICATION VISUALIZATIONS (300 DPI)")
    print("=" * 70)

    # -------------------------------------------------------------
    # Figure 1: Bar Chart Comparing Average PM2.5 Across Cities
    # -------------------------------------------------------------
    print("[1] Generating Figure 1: City PM2.5 Comparison Bar Chart...")
    city_means = df.groupby(["city", "region"])["pm2_5_mean"].mean().reset_index()
    
    # Select top 10 most polluted and top 10 cleanest
    top_10 = city_means.sort_values(by="pm2_5_mean", ascending=False).head(10)
    bottom_10 = city_means.sort_values(by="pm2_5_mean", ascending=True).head(10)
    combined = pd.concat([top_10, bottom_10]).sort_values(by="pm2_5_mean", ascending=True)

    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    colors = ["#2b83ba" if x < 25 else "#d7191c" for x in combined["pm2_5_mean"]]
    
    bars = ax.barh(combined["city"], combined["pm2_5_mean"], color=colors, edgecolor="#222222", height=0.65)
    
    # Reference benchmark lines
    ax.axvline(40, color="#d95f02", linestyle="--", linewidth=1.5, label="CPCB NAAQS Annual Limit (40 µg/m³)")
    ax.axvline(5, color="#1b9e77", linestyle=":", linewidth=1.5, label="WHO Air Quality Guideline (5 µg/m³)")

    # Data value labels on bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.8, bar.get_y() + bar.get_height() / 2, f"{width:.1f}", 
                va="center", ha="left", fontsize=9, fontweight="bold", color="#333333")

    ax.set_title("Average PM2.5 Concentration: Top 10 Most Polluted vs Top 10 Cleanest Cities (2022–2026)", 
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Mean PM2.5 Concentration (µg/m³)", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("City", fontsize=11, fontweight="bold")
    ax.set_xlim(0, max(combined["pm2_5_mean"]) + 10)
    ax.legend(frameon=True, facecolor="white", loc="lower right", fontsize=10)
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()

    fig1_path = os.path.join(FIGURES_DIR, "fig1_city_pm25_comparison.png")
    fig.savefig(fig1_path, dpi=300)
    plt.close(fig)
    print(f"  -> Saved to {fig1_path}")

    # -------------------------------------------------------------
    # Figure 2: Line Chart Showing Air Quality Trends Over Time
    # -------------------------------------------------------------
    print("[2] Generating Figure 2: Longitudinal Air Quality Trend Line Chart...")
    monthly_series = df.set_index("date").resample("ME")[["pm2_5_mean", "pm10_mean", "india_aqi"]].mean().reset_index()

    fig, ax1 = plt.subplots(figsize=(14, 6), dpi=300)
    
    color_pm25 = "#e41a1c"
    color_pm10 = "#377eb8"
    color_aqi = "#ff7f00"

    ax1.plot(monthly_series["date"], monthly_series["pm2_5_mean"], color=color_pm25, 
             marker="o", linewidth=2.2, label="PM2.5 Mean (µg/m³)")
    ax1.plot(monthly_series["date"], monthly_series["pm10_mean"], color=color_pm10, 
             marker="s", linewidth=2.0, linestyle="--", label="PM10 Mean (µg/m³)")
    ax1.set_xlabel("Observation Month (2022–2026)", fontsize=11, fontweight="bold", labelpad=10)
    ax1.set_ylabel("Particulate Concentration (µg/m³)", fontsize=11, fontweight="bold", color="#333333")
    ax1.tick_params(axis="y")

    # Secondary y-axis for India AQI
    ax2 = ax1.twinx()
    ax2.plot(monthly_series["date"], monthly_series["india_aqi"], color=color_aqi, 
             marker="^", linewidth=2.0, linestyle="-.", label="India AQI Index")
    ax2.set_ylabel("National AQI Scale (0–500)", fontsize=11, fontweight="bold", color=color_aqi)
    ax2.tick_params(axis="y", labelcolor=color_aqi)

    # Shading winter months (Dec-Jan) to highlight recurring seasonal smog peaks
    for year in [2022, 2023, 2024, 2025]:
        start_winter = pd.Timestamp(f"{year}-11-01")
        end_winter = pd.Timestamp(f"{year+1}-02-01")
        if start_winter >= monthly_series["date"].min() and start_winter <= monthly_series["date"].max():
            ax1.axvspan(start_winter, min(end_winter, monthly_series["date"].max()), 
                        color="gray", alpha=0.15, label="Winter Smog Season" if year == 2023 else "")

    # Combine legends
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper right", frameon=True, facecolor="white")

    ax1.set_title("Longitudinal Air Quality Dynamics in India: Monthly PM2.5, PM10, and AQI Trajectory", 
                  fontsize=13, fontweight="bold", pad=15)
    ax1.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    fig2_path = os.path.join(FIGURES_DIR, "fig2_air_quality_trend_over_time.png")
    fig.savefig(fig2_path, dpi=300)
    plt.close(fig)
    print(f"  -> Saved to {fig2_path}")

    # -------------------------------------------------------------
    # Figure 3: Histogram of Pollutant Distribution
    # -------------------------------------------------------------
    print("[3] Generating Figure 3: Pollutant Distribution Histogram with KDE...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

    # Subplot A: PM2.5 Distribution
    sns.histplot(df["pm2_5_mean"], bins=50, kde=True, ax=ax1, color="#2b83ba", edgecolor="#1a5276", alpha=0.6)
    mean_pm25 = df["pm2_5_mean"].mean()
    median_pm25 = df["pm2_5_mean"].median()
    p95_pm25 = df["pm2_5_mean"].quantile(0.95)

    ax1.axvline(mean_pm25, color="red", linestyle="--", linewidth=1.8, label=f"Mean: {mean_pm25:.1f} µg/m³")
    ax1.axvline(median_pm25, color="green", linestyle="-", linewidth=1.8, label=f"Median: {median_pm25:.1f} µg/m³")
    ax1.axvline(p95_pm25, color="purple", linestyle=":", linewidth=1.8, label=f"95th Pct: {p95_pm25:.1f} µg/m³")

    ax1.set_title("Distribution of Daily Mean PM2.5 Concentrations (N=77,150)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("PM2.5 Concentration (µg/m³)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Observation Frequency", fontsize=10, fontweight="bold")
    ax1.legend(frameon=True, facecolor="white", loc="upper right")
    ax1.grid(True, linestyle="--", alpha=0.5)

    # Subplot B: India AQI Distribution
    sns.histplot(df["india_aqi"], bins=40, kde=True, ax=ax2, color="#fdae61", edgecolor="#d95f02", alpha=0.6)
    mean_aqi = df["india_aqi"].mean()
    median_aqi = df["india_aqi"].median()

    ax2.axvline(mean_aqi, color="red", linestyle="--", linewidth=1.8, label=f"Mean: {mean_aqi:.1f}")
    ax2.axvline(median_aqi, color="green", linestyle="-", linewidth=1.8, label=f"Median: {median_aqi:.1f}")
    ax2.axvline(100, color="orange", linestyle=":", linewidth=1.5, label="Satisfactory Limit (100)")
    ax2.axvline(200, color="darkred", linestyle=":", linewidth=1.5, label="Moderate Limit (200)")

    ax2.set_title("Distribution of Daily National AQI Index (N=77,150)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("India National Air Quality Index (NAQI)", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Observation Frequency", fontsize=10, fontweight="bold")
    ax2.legend(frameon=True, facecolor="white", loc="upper right")
    ax2.grid(True, linestyle="--", alpha=0.5)

    plt.suptitle("Univariate Statistical Distributions and Skewness of Key Air Quality Parameters", 
                 fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()

    fig3_path = os.path.join(FIGURES_DIR, "fig3_pollutant_distribution_histogram.png")
    fig.savefig(fig3_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> Saved to {fig3_path}")

    # -------------------------------------------------------------
    # Figure 4: Scatter Plot of Weather Variable vs Air Quality
    # -------------------------------------------------------------
    print("[4] Generating Figure 4: Weather vs Air Quality Scatter Plot...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

    # Sample for performant scatter rendering with high statistical fidelity
    sample_df = df.sample(n=min(5000, len(df)), random_state=42)

    # Scatter A: Wind Speed vs PM2.5
    sns.regplot(data=sample_df, x="wind_speed_10m_max", y="pm2_5_mean", ax=ax1,
                scatter_kws={"alpha": 0.25, "color": "#1f78b4", "s": 15},
                line_kws={"color": "#e31a1c", "linewidth": 2.2})
    r_wind = np.corrcoef(df["wind_speed_10m_max"], df["pm2_5_mean"])[0, 1]
    ax1.set_title(f"Maximum Wind Speed vs PM2.5 (r = {r_wind:+.3f})", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Maximum Wind Speed at 10m (km/h)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Daily Mean PM2.5 (µg/m³)", fontsize=10, fontweight="bold")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.text(0.05, 0.90, "Dispersion Effect:\nStronger winds facilitate\npollutant dilution", 
             transform=ax1.transAxes, fontsize=9, bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.8))

    # Scatter B: Mean Temperature vs PM2.5
    sns.regplot(data=sample_df, x="temperature_2m_mean", y="pm2_5_mean", ax=ax2,
                scatter_kws={"alpha": 0.25, "color": "#ff7f00", "s": 15},
                line_kws={"color": "#33a02c", "linewidth": 2.2})
    r_temp = np.corrcoef(df["temperature_2m_mean"], df["pm2_5_mean"])[0, 1]
    ax2.set_title(f"Mean Ambient Temperature vs PM2.5 (r = {r_temp:+.3f})", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Daily Mean Temperature (°C)", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Daily Mean PM2.5 (µg/m³)", fontsize=10, fontweight="bold")
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.text(0.05, 0.90, "Thermal Inversion Effect:\nLower temperatures trap\nsurface emissions", 
             transform=ax2.transAxes, fontsize=9, bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.8))

    plt.suptitle("Meteorological Drivers of Particulate Pollution: Wind Dispersion and Thermal Inversion", 
                 fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()

    fig4_path = os.path.join(FIGURES_DIR, "fig4_weather_airquality_scatter.png")
    fig.savefig(fig4_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> Saved to {fig4_path}")

    # -------------------------------------------------------------
    # Figure 5: Correlation Heatmap
    # -------------------------------------------------------------
    print("[5] Generating Figure 5: Pearson Correlation Heatmap...")
    corr_cols = [
        "pm2_5_mean", "pm10_mean", "no2_mean", "so2_mean", "o3_8h_max", "co_8h_max", "india_aqi",
        "temperature_2m_mean", "relative_humidity_2m_mean", "wind_speed_10m_max", "precipitation_sum"
    ]
    corr_labels = [
        "PM2.5", "PM10", "NO2", "SO2", "O3 (8h)", "CO (8h)", "India AQI",
        "Temperature", "Humidity", "Wind Speed", "Precipitation"
    ]

    corr = df[corr_cols].corr(method="pearson")
    corr.columns = corr_labels
    corr.index = corr_labels

    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    sns.heatmap(corr, mask=mask, cmap="coolwarm", vmin=-1, vmax=1, center=0,
                annot=True, fmt=".2f", square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
                annot_kws={"size": 9, "fontweight": "bold"}, ax=ax)

    ax.set_title("Pearson Correlation Matrix: Air Pollutants & Meteorological Factors", 
                 fontsize=13, fontweight="bold", pad=15)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()

    fig5_path = os.path.join(FIGURES_DIR, "fig5_correlation_heatmap.png")
    fig.savefig(fig5_path, dpi=300)
    plt.close(fig)
    print(f"  -> Saved to {fig5_path}")

    # -------------------------------------------------------------
    # Figure 6: Regional & Seasonal Dynamics Boxplot
    # -------------------------------------------------------------
    print("[6] Generating Figure 6: Regional and Seasonal Dynamics...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)

    # Subplot A: Regional PM2.5 Boxplot
    order_regions = df.groupby("region")["pm2_5_mean"].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x="region", y="pm2_5_mean", order=order_regions, 
                hue="region", palette="Set2", legend=False, showfliers=False, ax=ax1)
    ax1.set_title("Regional Comparison of Daily PM2.5 Concentrations", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Geographic Region", fontsize=10, fontweight="bold")
    ax1.set_ylabel("PM2.5 Concentration (µg/m³)", fontsize=10, fontweight="bold")
    ax1.grid(True, linestyle="--", alpha=0.5)

    # Subplot B: Seasonal PM2.5 Distribution
    season_order = ["Winter", "Summer / Pre-Monsoon", "Monsoon", "Post-Monsoon"]
    sns.boxplot(data=df, x="season", y="pm2_5_mean", order=season_order, 
                hue="season", palette="Spectral", legend=False, showfliers=False, ax=ax2)
    ax2.set_title("Seasonal Variation in Daily PM2.5 (IMD Standard Classification)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Season", fontsize=10, fontweight="bold")
    ax2.set_ylabel("PM2.5 Concentration (µg/m³)", fontsize=10, fontweight="bold")
    ax2.grid(True, linestyle="--", alpha=0.5)

    plt.suptitle("Macro-Level Spatial and Temporal Variations in Indian Air Pollution", 
                 fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()

    fig6_path = os.path.join(FIGURES_DIR, "fig6_regional_seasonal_dynamics.png")
    fig.savefig(fig6_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> Saved to {fig6_path}")

    print("=" * 70)
    print("ALL VISUALIZATIONS GENERATED & SAVED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    generate_all_figures()
