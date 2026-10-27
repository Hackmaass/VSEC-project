---
license: cc-by-4.0
language:
  - en
pretty_name: India Daily Weather & Air Quality (Auto-Updated)
size_categories:
  - 100K<n<1M
task_categories:
  - time-series-forecasting
  - tabular-regression
tags:
  - weather
  - climate
  - air-quality
  - pollution
  - aqi
  - india
  - time-series
configs:
  - config_name: weather
    data_files: weather_daily.csv
    default: true
  - config_name: air_quality
    data_files: air_quality_daily.csv
  - config_name: cities
    data_files: cities.csv
---

# India Daily Weather & Air Quality (Auto-Updated)

Also on Kaggle: [kaggle.com/datasets/akshaykarthickms007/india-daily-weather-and-air-quality](https://www.kaggle.com/datasets/akshaykarthickms007/india-daily-weather-and-air-quality)

Daily **weather** and **air quality** for **50 Indian cities**, covering every region
from Leh to Port Blair. The dataset **updates automatically every day**.

| File | Rows | Coverage |
|---|---:|---|
| `weather_daily.csv` | 124,500 | 2020-01-01 → 2026-10-25 |
| `air_quality_daily.csv` | 77,150 | 2022-08-05 → 2026-10-25 |
| `cities.csv` | 50 | city, state, region, coordinates, elevation |

Last updated: **2026-10-26**. Weather history is being extended back to 2020-01-01,
about one year per day.

Highest average PM-based AQI: Agra (191), Delhi (182), Kanpur (137), Ludhiana (136), Amritsar (132). Lowest: Leh (10), Port Blair (19), Thiruvananthapuram (30), Coimbatore (30), Mysuru (31).

## Ideas

- Winter smog in the Indo-Gangetic plain: when does PM2.5 spike, and how does it relate to
  wind speed, temperature inversions and Diwali?
- Heatwaves: days with `temperature_2m_max` ≥ 45 °C, and how `apparent_temperature_max`
  compares across humid coastal and dry inland cities.
- Monsoon onset and withdrawal dates from `precipitation_sum`, by region.
- Forecast tomorrow's PM2.5 from today's weather and air quality (time-series ML).
- Dust storms: `dust_mean` and `aod_mean` over Rajasthan and the north-west.

## Models and notebooks using this dataset

- **Model:** [pm25-next-day-india](https://huggingface.co/AkshayKarthick/pm25-next-day-india),
  a LightGBM model that forecasts tomorrow's PM2.5 for all 50 cities, with a full model card.
- **Notebook:** [Forecasting tomorrow's PM2.5 in 50 Indian cities](https://www.kaggle.com/code/akshaykarthickms007/forecasting-tomorrow-s-pm2-5-in-50-indian-cities)
- **Notebook:** [India's Air & Weather: a Starter Analysis](https://www.kaggle.com/code/akshaykarthickms007/india-s-air-weather-a-starter-analysis)

## Files and columns

Join the files on `city` (and `date` for the two daily files).

### weather_daily.csv
| Column | Description |
|---|---|
| `date` | Local date (Asia/Kolkata) |
| `city` | City name (join key to cities.csv) |
| `temperature_2m_max` | Maximum air temperature at 2 m (°C) |
| `temperature_2m_min` | Minimum air temperature at 2 m (°C) |
| `temperature_2m_mean` | Mean air temperature at 2 m (°C) |
| `apparent_temperature_max` | Maximum feels-like temperature including humidity and wind (°C) |
| `precipitation_sum` | Total precipitation (mm) |
| `precipitation_hours` | Hours with precipitation (h) |
| `relative_humidity_2m_mean` | Mean relative humidity at 2 m (%) |
| `wind_speed_10m_max` | Maximum wind speed at 10 m (km/h) |
| `wind_direction_10m_dominant` | Dominant wind direction (° from north) |
| `shortwave_radiation_sum` | Total solar radiation (MJ/m²) |
| `et0_fao_evapotranspiration` | Reference evapotranspiration, FAO-56 (mm) |
| `weather_code` | Most severe WMO weather code of the day (0 clear … 95+ thunderstorm) |

### air_quality_daily.csv
| Column | Description |
|---|---|
| `date` | Local date (Asia/Kolkata) |
| `city` | City name (join key to cities.csv) |
| `pm2_5_mean` | 24-hour mean PM2.5 (µg/m³) |
| `pm2_5_max` | Highest hourly PM2.5 (µg/m³) |
| `pm10_mean` | 24-hour mean PM10 (µg/m³) |
| `pm10_max` | Highest hourly PM10 (µg/m³) |
| `no2_mean` | 24-hour mean nitrogen dioxide (µg/m³) |
| `so2_mean` | 24-hour mean sulphur dioxide (µg/m³) |
| `o3_8h_max` | Highest 8-hour mean ozone (µg/m³) |
| `co_8h_max` | Highest 8-hour mean carbon monoxide (µg/m³) |
| `dust_mean` | 24-hour mean dust (µg/m³) |
| `aod_mean` | Mean aerosol optical depth at 550 nm |
| `us_aqi_max` | Highest hourly US EPA AQI |
| `hours_available` | Hours of model data behind the daily values (days with < 18 are dropped) |
| `india_aqi` | Indian National AQI (CPCB formula, all pollutants). See the ozone caveat |
| `india_aqi_category` | Good / Satisfactory / Moderate / Poor / Very Poor / Severe |
| `dominant_pollutant` | Pollutant with the highest sub-index |
| `india_aqi_pm` | Indian AQI from PM2.5 and PM10 only (recommended; see caveat) |
| `india_aqi_pm_category` | Category of india_aqi_pm |

### cities.csv
| Column | Description |
|---|---|
| `city` | City name |
| `state` | State or union territory |
| `region` | North / South / East / West / Central / Northeast |
| `latitude` | Latitude used for the query (city centre) |
| `longitude` | Longitude used for the query (city centre) |
| `elevation_m` | Elevation of the model grid point in metres |

## How the Indian AQI is computed

Open-Meteo provides European and US AQI but not India's. This dataset adds the
**CPCB National AQI**:
- PM2.5, PM10, NO₂ and SO₂ use 24-hour means. O₃ and CO use the highest 8-hour mean.
- Each pollutant gets a sub-index by linear interpolation between the CPCB breakpoints.
- The AQI is the highest sub-index, reported when at least 3 pollutants, including PM, are available.
- The top "Severe" band is extended linearly and capped at 500.

**Ozone caveat.** The air-quality values come from the CAMS global model, not ground stations.
CAMS is known to overestimate surface ozone over India, so O₃ is the dominant pollutant on
90.2% of days in `india_aqi`, which pushes that index higher than CPCB station
readings. **For most analyses, use `india_aqi_pm`**, which is computed from PM2.5 and PM10 only.

## Sources and method

- **Weather:** [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api).
  It combines ECMWF IFS and ERA5/ERA5-Land reanalysis from the Copernicus Climate Change Service,
  with a resolution of about 9–25 km.
- **Air quality:** [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api).
  This is the Copernicus Atmosphere Monitoring Service (CAMS) global model at about 45 km. Its
  history for India starts in August 2022.
- Values are for the model grid cell at each city centre, aggregated to local days (IST).
- **Updates:** a GitHub Actions job runs every day. It re-downloads the last 10 days, because
  recent values are provisional and get revised, adds new days, validates the data, and
  publishes a new version. Validation covers missing days, duplicates, value ranges and stale cities.

## Limitations

- This is **model and reanalysis data, not station measurements**. It is smooth over 9–45 km
  and can miss very local effects, like a single busy road or an industrial area.
- The last ~10 days are provisional and can change slightly in later versions.
- Model ozone runs high over India (see above). Model PM tends to be less extreme than
  station peaks in severe winter smog.

## License and attribution

**CC BY 4.0.** Please credit:
- Weather data by [Open-Meteo.com](https://open-meteo.com/), with ERA5 from the Copernicus
  Climate Change Service.
- Air quality data by [Open-Meteo.com](https://open-meteo.com/) and the
  Copernicus Atmosphere Monitoring Service (CAMS).
- Indian AQI calculation and dataset by [AkshayKarthick](https://huggingface.co/AkshayKarthick).

The pipeline code (`update.py`, `naqi.py`, `cities.py`, `publish.py`) is included.

```python
from datasets import load_dataset

weather = load_dataset("AkshayKarthick/india-weather-air-quality", "weather", split="train").to_pandas()
aq = load_dataset("AkshayKarthick/india-weather-air-quality", "air_quality", split="train").to_pandas()
df = weather.merge(aq, on=["city", "date"])
```
