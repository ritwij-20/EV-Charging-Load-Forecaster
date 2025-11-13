# handlers.py
from datetime import timedelta
import pandas as pd
from data_utils import load_prophet_forecast, load_hourly, load_xgb_predictions
from prompts import TEMPLATE_FORECAST_NEXT_HOUR, TEMPLATE_EXPLAIN_PREDICTION, TEMPLATE_PEAK_HOURS, SYSTEM_PROMPT
from llm_client import ask_llm

def get_yesterday_actual(ts, hourly_df):
    # ts is pandas Timestamp
    prev = ts - pd.Timedelta(days=1)
    if prev in hourly_df.index:
        return float(hourly_df.loc[prev, "energy_kwh"])
    return None

def forecast_next_hour_handler():
    try:
        pf = load_prophet_forecast()
    except FileNotFoundError:
        return "prophet_forecast.csv not found. Generate Prophet forecast first."

    # predict next hour as last index + 1h
    next_hour = pf.index.max() + pd.Timedelta(hours=1)
    if next_hour not in pf.index:
        # fallback: return last yhat
        row = pf.iloc[-1]
        ts = row.name
        yhat = row.get("yhat", None)
    else:
        row = pf.loc[next_hour]
        ts = next_hour
        yhat = row.get("yhat")

    try:
        hourly = load_hourly()
        y_yesterday = get_yesterday_actual(ts, hourly)
    except FileNotFoundError:
        y_yesterday = None

    context = f"Predicted {yhat:.2f} kWh for {ts} (Prophet)."
    if y_yesterday is not None:
        context += f" Yesterday at same hour actual was {y_yesterday:.2f} kWh."

    prompt = TEMPLATE_FORECAST_NEXT_HOUR.format(context=context, ts=ts)
    return ask_llm(SYSTEM_PROMPT, prompt)

def peak_hours_handler(period_days: int = 7):
    try:
        hourly = load_hourly()
    except FileNotFoundError:
        return "hourly_ev_load.csv not found."

    end = hourly.index.max()
    start = end - pd.Timedelta(days=period_days)
    sub = hourly.loc[start:end]
    if sub.empty:
        return "No hourly data in the requested period."

    # compute average energy by hour of day
    avg_by_hour = sub.groupby(sub.index.hour)["energy_kwh"].mean().sort_values(ascending=False)
    top3 = avg_by_hour.head(3)
    context = "Top hours (hour, avg_kWh):\n" + top3.to_string()
    prompt = TEMPLATE_PEAK_HOURS.format(context=context)
    return ask_llm(SYSTEM_PROMPT, prompt)

def explain_prediction_handler(ts_str: str):
    """
    ts_str: 'YYYY-MM-DD HH:MM:SS' or ISO format string. This handler will attempt to explain model output.
    """
    try:
        hourly = load_hourly()
    except FileNotFoundError:
        return "hourly_ev_load.csv not found."

    try:
        ts = pd.to_datetime(ts_str)
    except Exception:
        return "Invalid timestamp format. Use 'YYYY-MM-DD HH:MM:SS'."

    # try to find xgb predictions if available
    try:
        xgb = load_xgb_predictions()
        if ts in xgb.index:
            row = xgb.loc[ts]
            # assume xgb_predictions.csv contains columns: y_pred, y_true, top_features (optional)
            y_pred = row.get("y_pred", None)
            y_true = row.get("y_true", None)
            top_feats = row.get("top_features", None)  # optional precomputed shap summary
            context = f"XGB predicted {y_pred} kWh; actual {y_true} kWh. Top features: {top_feats}"
        else:
            context = f"No xgb prediction for {ts} in xgb_predictions.csv"
    except FileNotFoundError:
        # fallback to prophet
        try:
            pf = load_prophet_forecast()
            if ts in pf.index:
                yhat = pf.loc[ts, "yhat"]
                context = f"Prophet predicted {yhat:.2f} kWh for {ts}."
            else:
                context = "No prediction found for that timestamp."
        except FileNotFoundError:
            return "No forecast files found (prophet_forecast.csv or xgb_predictions.csv)."

    prompt = TEMPLATE_EXPLAIN_PREDICTION.format(context=context, ts=ts)
    return ask_llm(SYSTEM_PROMPT, prompt)
