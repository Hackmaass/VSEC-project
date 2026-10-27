"""
Unit Tests for Visualization Generation
Project: Indian Air Quality and Weather Pattern Analysis Using Python
"""

import os
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES_DIR = os.path.join(BASE_DIR, "outputs", "figures")

EXPECTED_FIGURES = [
    "fig1_city_pm25_comparison.png",
    "fig2_air_quality_trend_over_time.png",
    "fig3_pollutant_distribution_histogram.png",
    "fig4_weather_airquality_scatter.png",
    "fig5_correlation_heatmap.png",
    "fig6_regional_seasonal_dynamics.png"
]

def test_all_expected_figures_exist():
    """Verify that all mandatory figures exist in outputs/figures/."""
    for fig_name in EXPECTED_FIGURES:
        fig_path = os.path.join(FIGURES_DIR, fig_name)
        assert os.path.exists(fig_path), f"Expected figure missing: {fig_path}"

def test_figures_have_valid_file_size():
    """Verify that figures are high-resolution (greater than 100 KB)."""
    for fig_name in EXPECTED_FIGURES:
        fig_path = os.path.join(FIGURES_DIR, fig_name)
        file_size = os.path.getsize(fig_path)
        assert file_size > 100000, f"Figure {fig_name} is unexpectedly small ({file_size} bytes), check DPI rendering"

def test_figures_are_valid_png():
    """Verify PNG header magic bytes (0x89 0x50 0x4E 0x47)."""
    for fig_name in EXPECTED_FIGURES:
        fig_path = os.path.join(FIGURES_DIR, fig_name)
        with open(fig_path, "rb") as f:
            header = f.read(8)
            assert header[:4] == b"\x89PNG", f"File {fig_name} is not a valid PNG image"
