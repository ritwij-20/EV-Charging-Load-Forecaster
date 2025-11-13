# data_utils.py
"""
Utility loaders for EV Load Forecaster.
Matches your dataset columns exactly:
- ev_charging_patterns.csv
- hourly_ev_load.csv
"""

import pandas as pd
from pathlib import Path
import datetime

DATA_DIR = Path(".")

def _safe_read(path):
    p = DATA_DIR / path
    if not p.exists():
        return None
    try:
        return pd.read_csv(p)
    except Exception:
        return pd.read_csv(p, engine="python")


# ------------------------------------------------------------
# LOAD HOURLY DATA (hourly_ev_load.csv)
# ------------------------------------------------------------
def load_hourly(path="hourly_ev_load.csv"):
    df = _safe_read(path)
    if df is None:
        return None

    # timestamp column
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    df = df.dropna(subset=["timestamp"])

    # energy column
    if "energy_kwh" in df.columns:
        df["energy_kwh"] = pd.to_numeric(df["energy_kwh"], errors="coerce").fillna(0.0)

    return df


# ------------------------------------------------------------
# LOAD SESSION DATA (ev_charging_patterns.csv)
# ------------------------------------------------------------
def load_sessions(path="ev_charging_patterns.csv"):
    df = _safe_read(path)
    if df is None:
        return None

    # Standardize datetime columns
    # You confirmed your CSV has EXACTLY THESE:
    # Charging Start Time, Charging End Time
    if "Charging Start Time" in df.columns:
        df["Charging Start Time"] = pd.to_datetime(df["Charging Start Time"], errors="coerce")

    if "Charging End Time" in df.columns:
        df["Charging End Time"] = pd.to_datetime(df["Charging End Time"], errors="coerce")

    df = df.dropna(subset=["Charging Start Time"])

    # Charger Type (exists)
    if "Charger Type" not in df.columns:
        return df  # still return, but chatbot will give reduced advice

    # Charging Station ID (exists)
    # Energy Consumed (kWh) (exists)

    return df


# ------------------------------------------------------------
# GET TODAY DATE
# ------------------------------------------------------------
def today_date():
    return datetime.date.today()
