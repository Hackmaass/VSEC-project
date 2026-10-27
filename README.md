# Indian Air Quality and Weather Pattern Analysis Using Python
### College Mini-Project (Assignment 12) | Undergraduate Engineering Curriculum

[![Python 3.14](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.66-red.svg)](https://streamlit.io/)
[![Pytest Passing](https://img.shields.io/badge/Pytest-13%20Passed-brightgreen.svg)](https://pytest.org/)
[![Hugging Face Dataset](https://img.shields.io/badge/Hugging%20Face-india--weather--air--quality-orange.svg)](https://huggingface.co/datasets/AkshayKarthick/india-weather-air-quality)

---

## 1. Project Overview & Problem Statement

Air pollution is one of the most critical public health and environmental challenges confronting modern India. High ambient concentrations of particulate matter ($PM_{2.5}$ and $PM_{10}$), nitrogen dioxide ($NO_2$), and ground-level ozone ($O_3$) are linked to cardiopulmonary mortality, reduced life expectancy, and severe economic losses.

However, air pollution is not solely an emissions problem; it is intrinsically coupled with **meteorology and atmospheric physics**. High winds disperse particulates, monsoonal rainfall scrubs aerosols from the sky, and cold winter weather triggers shallow thermal inversions that trap surface pollutants near breathing height.

This project implements an end-to-end, reproducible, empirical data analysis and visualization pipeline in Python. By merging and analyzing **77,150 paired daily observations** across **50 major Indian cities** from **August 2022 to October 2026**, the project demystifies the spatiotemporal and meteorological drivers of air pollution for undergraduate engineering students.

---

## 2. Project Objectives

1. **Empirical Data Pipeline:** Retrieve and clean raw multi-table air quality, weather, and geographic datasets without fabricating statistics.
2. **Mathematical Rigor:** Apply explicit NumPy and Pandas functions to calculate sample mean, median, sample variance, sample standard deviation, and key percentiles ($P_{25}, P_{50}, P_{75}, P_{90}, P_{95}, P_{99}$).
3. **Meteorological Correlation:** Quantify linear associations between weather drivers (wind speed, ambient temperature, relative humidity, precipitation) and particulate pollution.
4. **Regulatory Benchmarking:** Compare city concentrations against Central Pollution Control Board (CPCB) National Ambient Air Quality Standards (NAAQS) and World Health Organization (WHO) guidelines.
5. **Publication Visualizations:** Generate six high-resolution figures (300 DPI) using Matplotlib and Seaborn.
6. **Interactive Exploration:** Deploy a responsive Streamlit dashboard (`app.py`) with KPI cards, multi-city filters, and instant dataset export.
7. **Automated Testing:** Validate data cleaning, math accuracy, and visual outputs via 13 automated unit tests in Pytest.

---

## 3. Dataset Source & Provenance

- **Primary Repository:** [Hugging Face: AkshayKarthick/india-weather-air-quality](https://huggingface.co/datasets/AkshayKarthick/india-weather-air-quality)
- **Retrieval Date:** October 27, 2026
- **Raw Files Utilized:**
  * `air_quality_daily.csv` (77,150 rows, 19 columns, SHA-256: `ae98a78c6251...`)
  * `weather_daily.csv` (124,500 rows, 14 columns, SHA-256: `ae1130564057...`)
  * `cities.csv` (50 cities metadata, 6 columns, SHA-256: `b21222072aed...`)
- **Temporal Span:** August 5, 2022 to October 25, 2026 (4.2 continuous years)
- **Spatial Coverage:** 50 cities across 30 Indian States and Union Territories

---

## 4. Technology Stack

- **Core Language:** Python 3.14.7 (64-bit)
- **Data Wrangling:** Pandas 3.1.0
- **Vectorized Mathematics:** NumPy 2.5.4
- **Visualization Suite:** Matplotlib 3.11.2 & Seaborn 0.13.2
- **Interactive Web App:** Streamlit 1.66.1
- **Literate Computing:** Jupyter Notebook 7.6.3 & IPyKernel
- **Quality Assurance:** Pytest 9.1.1
- **Document Generation:** Python-docx 1.2.0 & PyWin32 (Microsoft Word COM)

---

## 5. Repository Directory Structure

```text
air-quality-analysis/
├── app.py                                   # Streamlit interactive dashboard application
├── requirements.txt                         # Certified project dependencies
├── README.md                                # Comprehensive documentation & viva guide
├── .gitignore                               # Git exclusion rules
├── data/
│   ├── raw/                                 # Untouched raw CSV files & metadata
│   │   ├── air_quality_daily.csv            # 77,150 raw air quality records
│   │   ├── weather_daily.csv                # 124,500 raw meteorological records
│   │   ├── cities.csv                       # 50 cities geographic metadata
│   │   ├── metadata.json                    # Provenance manifest
│   │   └── README.md                        # Dataset source notes
│   └── processed/                           # Cleaned, joined & aggregated datasets
│       ├── india_air_quality_weather_merged.csv  # 77,150 merged records (44 columns)
│       ├── city_air_quality_summary.csv     # City-level aggregated metrics
│       ├── monthly_air_quality_weather.csv  # Longitudinal monthly aggregates
│       └── seasonal_air_quality_weather.csv # IMD seasonal aggregates
├── notebooks/
│   ├── air_quality_analysis.ipynb           # Fully executed explanatory notebook
│   └── generate_notebook.py                 # Reproducible notebook generator
├── src/
│   ├── __init__.py                          # Package initialization
│   ├── download_data.py                     # Data retrieval & checksum verification
│   ├── data_cleaning.py                     # Data cleaning, validation & feature pipeline
│   ├── analysis.py                          # Explicit NumPy & Pandas statistical computing
│   └── visualizations.py                    # Matplotlib & Seaborn 300 DPI plot generator
├── outputs/
│   ├── figures/                             # High-resolution publication figures (300 DPI)
│   │   ├── fig1_city_pm25_comparison.png    # Top 10 polluted vs cleanest cities
│   │   ├── fig2_air_quality_trend_over_time.png # Multi-year monthly trajectory
│   │   ├── fig3_pollutant_distribution_histogram.png # Distribution & skewness
│   │   ├── fig4_weather_airquality_scatter.png # Wind dispersion & temperature inversion
│   │   ├── fig5_correlation_heatmap.png     # Pearson correlation matrix
│   │   ├── fig6_regional_seasonal_dynamics.png # Regional & seasonal boxplots
│   │   ├── dashboard_view_kpi_overview.png  # Streamlit header & KPI card view
│   │   └── dashboard_view_sidebar_tabs.png  # Streamlit filters & tab navigation view
│   ├── metrics/                             # JSON machine-readable statistics
│   │   ├── cleaning_summary.json            # Before/after cleaning metrics
│   │   └── statistical_summary.json         # Complete numerical analysis results
│   └── reports/                             # Generated academic deliverables
│       ├── Indian_Air_Quality_Weather_Analysis_Report.docx # 20-Page College Report (DOCX)
│       ├── Indian_Air_Quality_Weather_Analysis_Report.pdf  # 20-Page College Report (PDF)
│       ├── univariate_statistical_summary.csv # Univariate properties table
│       ├── city_rankings.csv                # All 50 cities ranked by PM2.5
│       ├── regional_statistical_summary.csv # Regional comparison table
│       ├── seasonal_statistical_summary.csv # IMD seasonal comparison table
│       └── correlation_matrix.csv           # Pearson correlation matrix table
├── scripts/
│   ├── generate_academic_report.py          # DOCX & PDF academic report builder
│   └── generate_dashboard_images.py         # Dashboard visual capture script
└── tests/
    ├── conftest.py                          # Pytest path configuration
    ├── test_cleaning.py                     # Data cleaning & schema tests
    ├── test_analysis.py                     # Math calculation & ranking tests
    └── test_visualizations.py               # PNG format & DPI tests
```

---

## 6. Installation & Execution Guide

### Step 1: Clone or Navigate to Project
```powershell
cd "d:\Projects\VSec prject"
```

### Step 2: Create and Activate Virtual Environment (Recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Certified Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Execute Complete Analytical Pipeline
You can run each stage independently or sequentially:

```powershell
# 1. Download & verify raw dataset
python src/download_data.py

# 2. Run data cleaning, range validation & relational join
python src/data_cleaning.py

# 3. Compute explicit NumPy statistics, rankings & correlations
python src/analysis.py

# 4. Generate all 300 DPI publication visualizations
python src/visualizations.py

# 5. Run the automated test suite
pytest -v
```

### Step 5: Launch Interactive Streamlit Dashboard
```powershell
streamlit run app.py
```
Open your browser to: `http://localhost:8501`

### Step 6: Execute Jupyter Notebook
```powershell
jupyter notebook notebooks/air_quality_analysis.ipynb
```

### Step 7: Regenerate Academic DOCX & PDF Report
```powershell
python scripts/generate_academic_report.py
```

---

## 7. Key Empirical Findings (Real Data)

| Metric / Dimension | Computed Value | Physical / Environmental Significance |
| :--- | :--- | :--- |
| **Total Analyzed Observations** | 77,150 records | Continuous, multi-year empirical dataset across 50 cities |
| **National Mean $PM_{2.5}$** | **35.49 µg/m³** | Below annual limit of 40 µg/m³, but pulled down by southern/hill cities |
| **National Median $PM_{2.5}$** | **28.10 µg/m³** | Marked positive skewness ($Mean > Median$) due to episodic winter spikes |
| **95th Percentile $PM_{2.5}$** | **91.28 µg/m³** | On acute pollution days, citizens breathe > 2.2x the national safe limit |
| **Top Polluted City** | **Delhi (74.21 µg/m³)** | Exceeds CPCB NAAQS (40 µg/m³) by 85.5% and WHO guideline (5 µg/m³) by 14.8x |
| **Cleanest City** | **Leh (4.92 µg/m³)** | High-altitude Himalayan basin complying with WHO strict health guideline |
| **Indo-Gangetic Corridor** | Agra (69.57), Amritsar (65.44), Ludhiana (64.83), Patna (61.15) | Geographic basin trapping creates persistent northern smog corridor |
| **Southern Maritime Sanctuaries** | Port Blair (10.57), Thiruvananthapuram (17.07), Coimbatore (17.89), Mysuru (18.47) | Peninsular coastal winds promote rapid particulate dilution |
| **Wind Dispersion Correlation** | **$r = -0.313$** | Stronger wind gusts dilute surface particulate density (ventilation effect) |
| **Rain Washout Correlation** | **$r = -0.225$** | Monsoonal rainfall wet-scavenges aerosols, producing annual pollution minimums |
| **Temperature Inversion Correlation** | **$r = -0.172$** | Cold winter temperatures trigger shallow inversion lids trapping emissions |

---

## 8. Test Suite Verification Results

Running `pytest -v` executes 13 automated unit tests:

```text
tests/test_analysis.py::test_numpy_statistical_calculation_accuracy PASSED [  7%]
tests/test_analysis.py::test_summary_metrics_file_validity PASSED        [ 15%]
tests/test_analysis.py::test_meteorological_correlations_with_pm25 PASSED [ 23%]
tests/test_analysis.py::test_city_rankings_consistency PASSED            [ 30%]
tests/test_cleaning.py::test_raw_files_exist PASSED                      [ 38%]
tests/test_cleaning.py::test_processed_dataset_exists PASSED             [ 46%]
tests/test_cleaning.py::test_clean_dataset_shape_and_columns PASSED      [ 53%]
tests/test_cleaning.py::test_missing_values_and_null_integrity PASSED    [ 61%]
tests/test_cleaning.py::test_physical_range_constraints PASSED           [ 69%]
tests/test_cleaning.py::test_temporal_features_validity PASSED           [ 76%]
tests/test_visualizations.py::test_all_expected_figures_exist PASSED     [ 84%]
tests/test_visualizations.py::test_figures_have_valid_file_size PASSED   [ 92%]
tests/test_visualizations.py::test_figures_are_valid_png PASSED          [100%]

============================= 13 passed in 2.41s ==============================
```

---

## 9. Academic Deliverables & Generated Report

The project includes a 20-page formal college report generated in both **Microsoft Word (.docx)** and **Adobe Acrobat (.pdf)** formats:
- Location DOCX: `outputs/reports/Indian_Air_Quality_Weather_Analysis_Report.docx` (3.3 MB)
- Location PDF: `outputs/reports/Indian_Air_Quality_Weather_Analysis_Report.pdf` (5.3 MB)
- Page Count: **20 Full Pages**
- Structure: Exact 12 mandatory sections in strict sequence with embedded 300 DPI figures, statistical tables, and citations.

---

## 10. College Viva & Practical Demonstration Checklist

When presenting this mini-project in an academic practical or viva voce examination, use this checklist to guide your 5-minute presentation:

### Viva Presentation Script (5 Minutes)
1. **Minute 1 - Motivation & Dataset:** State the project title, dataset origin (Hugging Face / CPCB / Open-Meteo), and emphasize that you analyzed 77,150 real-world observations across 50 cities without synthetic data.
2. **Minute 2 - Data Cleaning & Schema:** Explain the composite key join on `['city', 'date']`, date parsing to `datetime64`, physical clipping of negative optical sensor drift, and IMD seasonal grouping.
3. **Minute 3 - Mathematical Rigor:** Highlight your explicit use of NumPy for Bessel-corrected variance ($s^2$), standard deviation, and the 95th percentile ($91.28\,\mu g/m^3$) to demonstrate understanding of skewed distributions.
4. **Minute 4 - Findings & Physical Drivers:** Explain why Delhi ($74.21\,\mu g/m^3$) is 15 times more polluted than Leh ($4.92\,\mu g/m^3$) due to Indo-Gangetic basin trapping versus Himalayan elevation. Explain why wind speed has a negative correlation ($r = -0.313$) due to ventilation.
5. **Minute 5 - Interactive Dashboard Demo:** Launch `streamlit run app.py`, demonstrate filtering by region (e.g., North vs South) and dynamic KPI updates, show the download button, and conclude with the 100% passing Pytest suite.

### Anticipated Viva Questions & Model Answers

- **Q1: Why did you use Bessel's correction ($N-1$) in your variance calculation?**  
  *Answer:* When calculating variance from sample data rather than an entire theoretical population, dividing by $N$ systematically underestimates the true population dispersion. Dividing by degrees of freedom ($N-1$) provides an unbiased estimator of variance.

- **Q2: Why is the median PM2.5 ($28.10\,\mu g/m^3$) lower than the mean ($35.49\,\mu g/m^3$)?**  
  *Answer:* Environmental pollutant distributions are right-skewed (log-normal). Severe episodic winter smog peaks pull the arithmetic mean upward, whereas the median reflects the true central tendency on typical days.

- **Q3: Does a negative correlation between wind speed and PM2.5 prove that wind causes clean air?**  
  *Answer:* No. Correlation measures statistical co-occurrence, not mathematical proof of causation. The physical explanation is atmospheric fluid mechanics: higher wind speeds increase planetary boundary layer ventilation volume, mechanically dispersing particulate mass.

- **Q4: How did you handle missing values during the relational merge?**  
  *Answer:* Because Open-Meteo weather records spanned 2020–2026 for all 50 cities, every one of the 77,150 air quality records had a 100% matched date/city pair, resulting in zero unhandled nulls post-merge.

---

## 11. Limitations & Responsible Interpretation

1. **Correlation vs Causation:** Statistical correlation must always be substantiated with atmospheric physical mechanisms.
2. **Spatial Granularity:** City-level daily aggregates average across multiple neighborhood monitoring stations, smoothing out hyper-local traffic intersection hotspots.
3. **Satellite vs Ground Sensors:** Satellite aerosol optical depth (AOD) retrievals complement ground monitors but can encounter data gaps during heavy monsoonal cloud cover.

---

## 12. References

1. Central Pollution Control Board (CPCB), *National Air Quality Index (NAQI) Technical Guidelines*, New Delhi, 2014.
2. World Health Organization (WHO), *Global Air Quality Guidelines*, Geneva, 2021.
3. Karthick, Akshay, *India Weather and Air Quality Dataset*, Hugging Face Datasets, 2026.
4. Open-Meteo, *Open-Source Weather API Documentation*, 2026.
5. McKinney, Wes, *Data Structures for Statistical Computing in Python*, SciPy, 2010.
6. Harris, C.R. et al., *Array programming with NumPy*, Nature, 2020.
7. Hunter, J.D., *Matplotlib: A 2D Graphics Environment*, IEEE, 2007.
8. Indian Meteorological Department (IMD), *Classification of Seasons and Climate of India*, Pune, 2021.
