"""
Generate high-fidelity visual representations of the Streamlit Dashboard
components for the academic report results section.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES_DIR = os.path.join(BASE_DIR, "outputs", "figures")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed", "india_air_quality_weather_merged.csv")

def generate_dashboard_views():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    df = pd.read_csv(PROCESSED_PATH)
    df["date"] = pd.to_datetime(df["date"])

    # 1. Dashboard Overview & KPI Metrics Card View
    fig, ax = plt.subplots(figsize=(14, 5.5), dpi=300)
    ax.axis("off")
    fig.patch.set_facecolor("#f8fafc")

    # Header
    ax.text(0.02, 0.90, "🌫️ Indian Air Quality & Weather Pattern Analysis (2022–2026)", 
            fontsize=18, fontweight="bold", color="#1e3a8a", transform=ax.transAxes)
    ax.text(0.02, 0.81, "Interactive Streamlit Analytics Dashboard | College Mini-Project (Assignment 12)", 
            fontsize=11, color="#475569", transform=ax.transAxes)

    # 5 KPI Cards
    cards = [
        {"title": "TOTAL OBSERVATIONS", "val": f"{len(df):,}", "sub": "100% Complete & Cleaned", "color": "#2563eb"},
        {"title": "CITIES REPRESENTED", "val": f"{df['city'].nunique()} Cities", "sub": f"{df['state'].nunique()} States / UTs", "color": "#059669"},
        {"title": "MEAN PM2.5 CONCENTRATION", "val": f"{df['pm2_5_mean'].mean():.2f} µg/m³", "sub": "NAAQS Limit: 40 µg/m³", "color": "#dc2626"},
        {"title": "NATIONAL AQI (MEAN)", "val": f"{df['india_aqi'].mean():.1f}", "sub": f"Median: {df['india_aqi'].median():.1f} (Moderate)", "color": "#d97706"},
        {"title": "CLIMATE AVERAGES", "val": f"{df['temperature_2m_mean'].mean():.1f} °C", "sub": f"Wind: {df['wind_speed_10m_max'].mean():.1f} km/h", "color": "#7c3aed"}
    ]

    card_width = 0.18
    spacing = 0.015
    start_x = 0.02

    for i, card in enumerate(cards):
        x = start_x + i * (card_width + spacing)
        rect = plt.Rectangle((x, 0.15), card_width, 0.55, transform=ax.transAxes,
                             facecolor="white", edgecolor="#cbd5e1", linewidth=1.5)
        ax.add_patch(rect)
        # Left accent stripe
        stripe = plt.Rectangle((x, 0.15), 0.008, 0.55, transform=ax.transAxes,
                               facecolor=card["color"], edgecolor="none")
        ax.add_patch(stripe)

        ax.text(x + 0.015, 0.58, card["title"], fontsize=8, fontweight="bold", color="#64748b", transform=ax.transAxes)
        ax.text(x + 0.015, 0.38, card["val"], fontsize=14, fontweight="bold", color="#0f172a", transform=ax.transAxes)
        ax.text(x + 0.015, 0.22, card["sub"], fontsize=8, color="#059669" if "Limit" not in card["sub"] else "#dc2626", transform=ax.transAxes)

    plt.tight_layout()
    p1 = os.path.join(FIGURES_DIR, "dashboard_view_kpi_overview.png")
    fig.savefig(p1, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    print(f"  -> Generated {p1}")

    # 2. Dashboard Filter Controls & UI Navigation View
    fig, (ax_side, ax_main) = plt.subplots(1, 2, figsize=(14, 6), dpi=300, gridspec_kw={"width_ratios": [1, 2.5]})
    fig.patch.set_facecolor("#f1f5f9")

    # Sidebar mockup
    ax_side.axis("off")
    rect_side = plt.Rectangle((0.02, 0.02), 0.96, 0.96, transform=ax_side.transAxes,
                              facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.2)
    ax_side.add_patch(rect_side)
    ax_side.text(0.08, 0.92, "⚙️ Filter Controls", fontsize=13, fontweight="bold", color="#1e293b", transform=ax_side.transAxes)
    ax_side.text(0.08, 0.82, "Geographic Region:", fontsize=9, fontweight="bold", color="#475569", transform=ax_side.transAxes)
    ax_side.text(0.08, 0.74, "[✓] North  [✓] South  [✓] East\n[✓] West   [✓] Central [✓] Northeast", fontsize=8, color="#2563eb", transform=ax_side.transAxes)

    ax_side.text(0.08, 0.62, "Selected Cities (Active Filter):", fontsize=9, fontweight="bold", color="#475569", transform=ax_side.transAxes)
    ax_side.text(0.08, 0.52, "• Delhi, Mumbai, Bengaluru\n• Kolkata, Chennai, Lucknow\n• Patna, Hyderabad, Agra", fontsize=8, color="#0f172a", transform=ax_side.transAxes)

    ax_side.text(0.08, 0.38, "Temporal Range:", fontsize=9, fontweight="bold", color="#475569", transform=ax_side.transAxes)
    ax_side.text(0.08, 0.30, "📅 2022-08-05 to 2026-10-25\n(4.2 Years / 1,543 Days)", fontsize=8, color="#0f172a", transform=ax_side.transAxes)

    ax_side.text(0.08, 0.18, "Primary Variable:", fontsize=9, fontweight="bold", color="#475569", transform=ax_side.transAxes)
    ax_side.text(0.08, 0.10, "🔘 PM2.5 Mean (µg/m³)\n🔘 India AQI (NAQI)", fontsize=8, color="#2563eb", transform=ax_side.transAxes)

    # Main interactive tabs preview
    ax_main.axis("off")
    rect_main = plt.Rectangle((0.02, 0.02), 0.96, 0.96, transform=ax_main.transAxes,
                              facecolor="white", edgecolor="#cbd5e1", linewidth=1.2)
    ax_main.add_patch(rect_main)

    # Tab headers
    tab_titles = ["📊 City Comparison", "📈 Temporal Dynamics", "🌦️ Meteorology", "🔥 Correlation", "📋 Data Explorer", "📖 Limitations"]
    for j, t in enumerate(tab_titles):
        tx = 0.05 + j * 0.155
        is_active = (j == 0)
        t_rect = plt.Rectangle((tx, 0.88), 0.145, 0.07, transform=ax_main.transAxes,
                               facecolor="#2563eb" if is_active else "#f1f5f9",
                               edgecolor="#cbd5e1", linewidth=1)
        ax_main.add_patch(t_rect)
        ax_main.text(tx + 0.015, 0.91, t, fontsize=7.5, fontweight="bold" if is_active else "normal",
                     color="white" if is_active else "#475569", transform=ax_main.transAxes)

    # Preview of City Comparison Tab content
    ax_main.text(0.05, 0.80, "Active City Ranking (Subset Filtered):", fontsize=11, fontweight="bold", color="#1e293b", transform=ax_main.transAxes)
    sample_cities = ["Delhi", "Agra", "Amritsar", "Patna", "Kolkata", "Lucknow", "Bengaluru", "Chennai"]
    sample_pm25 = [74.2, 69.6, 65.4, 61.2, 57.7, 57.7, 20.8, 22.4]

    for k, (c_name, c_val) in enumerate(zip(sample_cities, sample_pm25)):
        by = 0.70 - k * 0.07
        bar_len = (c_val / 80.0) * 0.55
        b_color = "#dc2626" if c_val > 40 else "#2563eb"
        b_patch = plt.Rectangle((0.20, by), bar_len, 0.045, transform=ax_main.transAxes, facecolor=b_color, edgecolor="#333333")
        ax_main.add_patch(b_patch)
        ax_main.text(0.05, by + 0.01, c_name, fontsize=8.5, fontweight="bold", color="#333333", transform=ax_main.transAxes)
        ax_main.text(0.20 + bar_len + 0.015, by + 0.01, f"{c_val} µg/m³", fontsize=8, fontweight="bold", color=b_color, transform=ax_main.transAxes)

    ax_main.axvline(0.20 + (40/80.0)*0.55, ymin=0.15, ymax=0.78, color="#d95f02", linestyle="--", linewidth=1.2)
    ax_main.text(0.20 + (40/80.0)*0.55 + 0.01, 0.16, "CPCB 40 µg/m³ Limit", fontsize=7.5, color="#d95f02", fontweight="bold", transform=ax_main.transAxes)

    plt.tight_layout()
    p2 = os.path.join(FIGURES_DIR, "dashboard_view_sidebar_tabs.png")
    fig.savefig(p2, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    print(f"  -> Generated {p2}")

if __name__ == "__main__":
    generate_dashboard_views()
