"""
Streamlit Interactive Dashboard
Project: Indian Air Quality and Weather Pattern Analysis Using Python
Author: Academic Mini Project Developer

Run command:
    streamlit run app.py
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(
    page_title="India Air Quality & Weather Analysis",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4b5563;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background-color: #f8fafc;
        border-radius: 10px;
        padding: 1.2rem;
        border-left: 5px solid #2563eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .kpi-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        color: #64748b;
        font-weight: 600;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
    }
    .kpi-sub {
        font-size: 0.8rem;
        color: #10b981;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "india_air_quality_weather_merged.csv")

@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"Processed dataset not found at {DATA_PATH}. Please run src/data_cleaning.py first.")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df

df_full = load_data()

# -------------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1163/1163657.png", width=60)
st.sidebar.title("Filter Controls")

# Region Filter
all_regions = sorted(df_full["region"].unique().tolist())
selected_regions = st.sidebar.multiselect("Select Geographic Regions", options=all_regions, default=all_regions)

# City Filter filtered by selected regions
available_cities = sorted(df_full[df_full["region"].isin(selected_regions)]["city"].unique().tolist())
default_cities = [c for c in ["Delhi", "Mumbai", "Bengaluru", "Kolkata", "Chennai", "Lucknow", "Patna", "Hyderabad", "Agra", "Amritsar"] if c in available_cities]
if not default_cities and available_cities:
    default_cities = available_cities[:8]

selected_cities = st.sidebar.multiselect(
    "Select Cities",
    options=available_cities,
    default=default_cities
)

# Date Range Filter
min_date = df_full["date"].min().date()
max_date = df_full["date"].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Primary Pollutant Metric Selector
pollutant_options = {
    "PM2.5 Mean (µg/m³)": "pm2_5_mean",
    "PM10 Mean (µg/m³)": "pm10_mean",
    "India AQI (NAQI)": "india_aqi",
    "Nitrogen Dioxide - NO2 (µg/m³)": "no2_mean",
    "Sulfur Dioxide - SO2 (µg/m³)": "so2_mean",
    "Ozone - O3 8h Max (µg/m³)": "o3_8h_max",
    "Carbon Monoxide - CO 8h Max (µg/m³)": "co_8h_max"
}
selected_pollutant_label = st.sidebar.selectbox("Primary Pollutant Variable", list(pollutant_options.keys()), index=0)
selected_pollutant_col = pollutant_options[selected_pollutant_label]

# Filter DataFrame
if len(date_range) == 2:
    start_d, end_d = date_range
else:
    start_d, end_d = min_date, max_date

df_filtered = df_full[
    (df_full["region"].isin(selected_regions)) &
    (df_full["city"].isin(selected_cities)) &
    (df_full["date"].dt.date >= start_d) &
    (df_full["date"].dt.date <= end_d)
].copy()

if df_filtered.empty:
    st.warning("No records match the current filter selection. Please broaden your filters in the sidebar.")
    st.stop()

# -------------------------------------------------------------
# MAIN CONTENT HEADER & KPI CARDS
# -------------------------------------------------------------
st.markdown('<div class="main-header">Indian Air Quality & Weather Pattern Analysis</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">An empirical college mini-project evaluating spatiotemporal pollutant concentrations, '
    'meteorological drivers, and CPCB compliance across 50 Indian cities (2022–2026).</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Records", f"{len(df_filtered):,}", delta=f"{len(df_filtered)/len(df_full)*100:.1f}% of total")
with col2:
    st.metric("Cities Filtered", f"{df_filtered['city'].nunique()} / {df_full['city'].nunique()}")
with col3:
    mean_val = df_filtered[selected_pollutant_col].mean()
    st.metric(f"Mean {selected_pollutant_col}", f"{mean_val:.2f}", 
              delta="High Concern" if (selected_pollutant_col == "pm2_5_mean" and mean_val > 40) else "Moderate")
with col4:
    mean_aqi = df_filtered["india_aqi"].mean()
    st.metric("Mean National AQI", f"{mean_aqi:.1f}", delta=f"P50: {df_filtered['india_aqi'].median():.1f}")
with col5:
    mean_temp = df_filtered["temperature_2m_mean"].mean()
    mean_wind = df_filtered["wind_speed_10m_max"].mean()
    st.metric("Mean Temp / Wind", f"{mean_temp:.1f} °C", delta=f"{mean_wind:.1f} km/h wind")

st.markdown("---")

# -------------------------------------------------------------
# TABS INTERFACE
# -------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 City Comparison",
    "📈 Temporal Dynamics",
    "🌦️ Weather & Meteorology",
    "🔥 Correlation & Distributions",
    "📋 Data Explorer & Download",
    "📖 Source & Limitations"
])

# TAB 1: CITY COMPARISON
with tab1:
    st.subheader(f"City-Wise Comparison: {selected_pollutant_label}")
    city_agg = df_filtered.groupby(["city", "region"])[selected_pollutant_col].mean().reset_index()
    city_agg = city_agg.sort_values(by=selected_pollutant_col, ascending=False)

    col_chart, col_rank = st.columns([2.5, 1.2])
    with col_chart:
        fig, ax = plt.subplots(figsize=(10, max(4, len(city_agg) * 0.35)), dpi=150)
        bars = ax.barh(city_agg["city"], city_agg[selected_pollutant_col], color="#2563eb", edgecolor="#1e3a8a", height=0.6)
        
        if selected_pollutant_col == "pm2_5_mean":
            ax.axvline(40, color="#dc2626", linestyle="--", label="CPCB Safe Limit (40 µg/m³)")
            ax.axvline(5, color="#16a34a", linestyle=":", label="WHO Guideline (5 µg/m³)")
            ax.legend(loc="lower right")

        for bar in bars:
            w = bar.get_width()
            ax.text(w + 0.5, bar.get_y() + bar.get_height()/2, f"{w:.1f}", va="center", fontsize=8, fontweight="bold")

        ax.set_xlabel(selected_pollutant_label, fontweight="bold")
        ax.set_ylabel("City", fontweight="bold")
        ax.set_title(f"Average {selected_pollutant_label} by City", fontweight="bold")
        ax.invert_yaxis()
        ax.grid(axis="x", linestyle="--", alpha=0.5)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col_rank:
        st.markdown("**Subset Top Polluted Cities**")
        st.dataframe(
            city_agg.head(5)[["city", selected_pollutant_col]].rename(columns={selected_pollutant_col: "Mean Value"}),
            hide_index=True
        )
        st.markdown("**Subset Cleanest Cities**")
        st.dataframe(
            city_agg.tail(5)[["city", selected_pollutant_col]].rename(columns={selected_pollutant_col: "Mean Value"}),
            hide_index=True
        )

# TAB 2: TEMPORAL DYNAMICS
with tab2:
    st.subheader("Longitudinal Trends and Seasonal Patterns")
    freq = st.radio("Aggregation Interval", ["Daily", "Weekly", "Monthly"], index=2, horizontal=True)
    rule_map = {"Daily": "D", "Weekly": "W-MON", "Monthly": "ME"}
    
    ts_df = df_filtered.set_index("date").resample(rule_map[freq])[
        ["pm2_5_mean", "pm10_mean", "india_aqi", "temperature_2m_mean"]
    ].mean().reset_index()

    fig, ax1 = plt.subplots(figsize=(12, 4.5), dpi=150)
    ax1.plot(ts_df["date"], ts_df["pm2_5_mean"], label="PM2.5 (µg/m³)", color="#e11d48", linewidth=2)
    ax1.plot(ts_df["date"], ts_df["pm10_mean"], label="PM10 (µg/m³)", color="#2563eb", linewidth=1.8, linestyle="--")
    ax1.set_xlabel("Date", fontweight="bold")
    ax1.set_ylabel("Particulate Concentration (µg/m³)", fontweight="bold")
    ax1.grid(True, linestyle="--", alpha=0.4)

    ax2 = ax1.twinx()
    ax2.plot(ts_df["date"], ts_df["india_aqi"], label="India AQI", color="#d97706", linewidth=1.8, linestyle="-.")
    ax2.set_ylabel("National AQI Index", color="#d97706", fontweight="bold")
    ax2.tick_params(axis="y", labelcolor="#d97706")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
    ax1.set_title(f"{freq} Trajectory of Air Quality Metrics in Selected Filter Domain", fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("### Seasonal Breakdown (Indian Meteorological Department Classification)")
    season_agg = df_filtered.groupby("season").agg(
        Records=("date", "count"),
        PM2_5_Mean=("pm2_5_mean", "mean"),
        PM10_Mean=("pm10_mean", "mean"),
        AQI_Mean=("india_aqi", "mean"),
        Temp_Mean=("temperature_2m_mean", "mean"),
        Wind_Mean=("wind_speed_10m_max", "mean")
    ).round(2).reset_index()
    st.dataframe(season_agg, hide_index=True)

# TAB 3: WEATHER & METEOROLOGY
with tab3:
    st.subheader("Meteorological Influences on Particulate Pollution")
    col_w1, col_w2 = st.columns(2)

    sample_size = min(3000, len(df_filtered))
    df_sample = df_filtered.sample(sample_size, random_state=42)

    with col_w1:
        st.markdown("#### Wind Speed vs PM2.5 (Atmospheric Dispersion)")
        fig, ax = plt.subplots(figsize=(6, 4.5), dpi=150)
        sns.regplot(data=df_sample, x="wind_speed_10m_max", y="pm2_5_mean", ax=ax,
                    scatter_kws={"alpha": 0.3, "color": "#2563eb", "s": 12},
                    line_kws={"color": "#dc2626", "linewidth": 2})
        r_w = np.corrcoef(df_filtered["wind_speed_10m_max"], df_filtered["pm2_5_mean"])[0, 1]
        ax.set_title(f"Wind Speed vs PM2.5 (r = {r_w:+.3f})", fontweight="bold")
        ax.set_xlabel("Wind Speed (km/h)", fontweight="bold")
        ax.set_ylabel("PM2.5 (µg/m³)", fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.4)
        st.pyplot(fig)
        plt.close(fig)
        st.info("**Physical Mechanism**: Higher horizontal wind velocities enhance turbulent atmospheric dispersion, "
                "diluting surface ground pollutant concentrations.")

    with col_w2:
        st.markdown("#### Ambient Temperature vs PM2.5 (Thermal Inversion)")
        fig, ax = plt.subplots(figsize=(6, 4.5), dpi=150)
        sns.regplot(data=df_sample, x="temperature_2m_mean", y="pm2_5_mean", ax=ax,
                    scatter_kws={"alpha": 0.3, "color": "#f59e0b", "s": 12},
                    line_kws={"color": "#16a34a", "linewidth": 2})
        r_t = np.corrcoef(df_filtered["temperature_2m_mean"], df_filtered["pm2_5_mean"])[0, 1]
        ax.set_title(f"Mean Temperature vs PM2.5 (r = {r_t:+.3f})", fontweight="bold")
        ax.set_xlabel("Temperature (°C)", fontweight="bold")
        ax.set_ylabel("PM2.5 (µg/m³)", fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.4)
        st.pyplot(fig)
        plt.close(fig)
        st.info("**Physical Mechanism**: Cold winter temperatures trigger surface boundary layer temperature inversions, "
                "trapping particulate matter close to breathing height.")

# TAB 4: CORRELATION & DISTRIBUTIONS
with tab4:
    st.subheader("Statistical Distributions & Pearson Correlation Heatmap")
    col_c1, col_c2 = st.columns([1.5, 1])

    with col_c1:
        st.markdown("#### Pearson Correlation Heatmap")
        corr_vars = [
            "pm2_5_mean", "pm10_mean", "no2_mean", "so2_mean", "o3_8h_max", "co_8h_max", "india_aqi",
            "temperature_2m_mean", "relative_humidity_2m_mean", "wind_speed_10m_max", "precipitation_sum"
        ]
        corr_labels = ["PM2.5", "PM10", "NO2", "SO2", "O3", "CO", "AQI", "Temp", "Humidity", "Wind", "Precip"]
        corr = df_filtered[corr_vars].corr(method="pearson")
        corr.columns = corr_labels
        corr.index = corr_labels

        fig, ax = plt.subplots(figsize=(7, 6), dpi=150)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1,
                    square=True, linewidths=0.5, cbar_kws={"shrink": 0.75},
                    annot_kws={"size": 7, "fontweight": "bold"}, ax=ax)
        plt.xticks(rotation=45, ha="right", fontsize=8)
        plt.yticks(rotation=0, fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col_c2:
        st.markdown("#### National AQI Category Breakdown")
        aqi_counts = df_filtered["india_aqi_category"].value_counts()
        fig, ax = plt.subplots(figsize=(5, 5), dpi=150)
        category_palette = {
            "Good": "#16a34a",
            "Satisfactory": "#84cc16",
            "Moderate": "#facc15",
            "Poor": "#f97316",
            "Very Poor": "#ef4444",
            "Severe": "#7f1d1d"
        }
        colors = [category_palette.get(c, "#94a3b8") for c in aqi_counts.index]
        ax.pie(aqi_counts, labels=aqi_counts.index, autopct="%1.1f%%", startangle=140, colors=colors,
               textprops={"fontsize": 9, "fontweight": "bold"})
        ax.set_title("AQI Category Share", fontweight="bold")
        st.pyplot(fig)
        plt.close(fig)

# TAB 5: DATA EXPLORER & DOWNLOAD
with tab5:
    st.subheader("Data Explorer and Verified Dataset Download")
    st.markdown(f"Displaying **{len(df_filtered):,}** records matching current filters.")

    preview_cols = [
        "date", "city", "state", "region", "pm2_5_mean", "pm10_mean", "india_aqi",
        "india_aqi_category", "dominant_pollutant", "temperature_2m_mean",
        "relative_humidity_2m_mean", "wind_speed_10m_max", "precipitation_sum", "season"
    ]
    st.dataframe(df_filtered[preview_cols].head(100), use_container_width=True)

    csv_data = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Cleaned Dataset (CSV)",
        data=csv_data,
        file_name="india_air_quality_weather_filtered.csv",
        mime="text/csv",
        help="Download the filtered data as a standard comma-separated values file."
    )

    st.markdown("### Descriptive Numerical Statistics Table")
    num_summary = df_filtered[[
        "pm2_5_mean", "pm10_mean", "no2_mean", "so2_mean", "o3_8h_max", "co_8h_max", "india_aqi",
        "temperature_2m_mean", "relative_humidity_2m_mean", "wind_speed_10m_max", "precipitation_sum"
    ]].describe().T[["count", "mean", "std", "min", "25%", "50%", "75%", "max"]]
    num_summary = num_summary.round(2)
    st.dataframe(num_summary, use_container_width=True)

# TAB 6: SOURCE & LIMITATIONS
with tab6:
    st.subheader("Methodology, Limitations & Dataset Provenance")
    st.markdown("""
    ### 1. Dataset Origin & Retrieval
    - **Primary Repository**: [AkshayKarthick/india-weather-air-quality](https://huggingface.co/datasets/AkshayKarthick/india-weather-air-quality)
    - **Retrieval Date**: October 27, 2026
    - **Raw Files Utilized**:
      * `air_quality_daily.csv` (77,150 rows, 19 columns, SHA-256 verified)
      * `weather_daily.csv` (124,500 rows, 14 columns, SHA-256 verified)
      * `cities.csv` (50 cities metadata, 6 columns)
    - **Temporal Coverage**: August 5, 2022 to October 25, 2026 (over 4 complete annual cycles)
    
    ### 2. Standards & Index Calculations
    - **National Air Quality Index (NAQI)**: Formulated in accordance with Central Pollution Control Board (CPCB) India guidelines.
    - **Meteorology Integration**: ERA5 reanalysis and Open-Meteo API daily aggregates paired with ground and satellite air quality monitoring.
    - **Seasons**: Indian Meteorological Department (IMD) standard 4-season definition.

    ### 3. Academic & Analytical Limitations
    - **Correlation vs Causation**: Statistical association (such as between wind speed and PM2.5) demonstrates physical co-occurrence, not mathematical proof of sole causation.
    - **Spatial Generalization**: City-wide daily averages smooth out micro-hotspots (e.g., traffic intersections vs vegetative parks).
    - **Satellite Calibration**: AOD and satellite aerosol retrievals complement ground monitors but are subject to cloud-cover interference during the southwest monsoon.
    """)

st.markdown("---")
st.caption("College Mini Project: Indian Air Quality and Weather Pattern Analysis Using Python | Built with Pandas, NumPy, Matplotlib, Seaborn, and Streamlit")
