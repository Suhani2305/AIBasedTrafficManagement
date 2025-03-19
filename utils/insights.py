import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

def generate_peak_hours_insight(hourly_pattern: pd.Series) -> str:
    """Generate insights about peak traffic hours."""
    peak_hour = hourly_pattern.idxmax()
    peak_volume = hourly_pattern.max()
    off_peak = hourly_pattern.idxmin()
    
    return f"""Peak traffic occurs at {peak_hour}:00 with an average volume of {int(peak_volume)} vehicles.
Best time for travel would be around {off_peak}:00 when traffic is lowest."""

def generate_weekly_pattern_insight(daily_pattern: pd.Series) -> str:
    """Generate insights about weekly traffic patterns."""
    busiest_day = daily_pattern.idxmax()
    quietest_day = daily_pattern.idxmin()
    avg_weekday = daily_pattern[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']].mean()
    avg_weekend = daily_pattern[['Saturday', 'Sunday']].mean()
    
    weekend_diff = ((avg_weekend - avg_weekday) / avg_weekday) * 100
    
    if weekend_diff < 0:
        weekend_pattern = f"Weekend traffic is {abs(weekend_diff):.1f}% lower than weekdays"
    else:
        weekend_pattern = f"Weekend traffic is {weekend_diff:.1f}% higher than weekdays"
    
    return f"""Busiest day: {busiest_day}
Quietest day: {quietest_day}
{weekend_pattern}"""

def analyze_traffic_trend(df: pd.DataFrame) -> str:
    """Analyze overall traffic trend."""
    recent_trend = df['traffic_volume'].tail(24).mean()
    past_trend = df['traffic_volume'].head(24).mean()
    
    percent_change = ((recent_trend - past_trend) / past_trend) * 100
    
    if abs(percent_change) < 5:
        trend = "relatively stable"
    elif percent_change > 0:
        trend = f"increasing by {percent_change:.1f}%"
    else:
        trend = f"decreasing by {abs(percent_change):.1f}%"
    
    return f"Traffic volume is {trend} compared to the previous period."

def generate_prediction_insight(predictions: np.ndarray) -> str:
    """Generate insights about traffic predictions."""
    peak_hour = predictions.argmax()
    peak_volume = predictions.max()
    quiet_hour = predictions.argmin()
    
    return f"""Tomorrow's peak traffic is expected at {peak_hour}:00 with approximately {int(peak_volume)} vehicles.
The quietest period is predicted to be at {quiet_hour}:00.
Plan your journey accordingly to avoid peak congestion."""

def get_all_insights(df: pd.DataFrame, hourly_pattern: pd.Series, 
                    daily_pattern: pd.Series, predictions: np.ndarray) -> Dict[str, str]:
    """Generate all insights for the dashboard."""
    return {
        'trend': analyze_traffic_trend(df),
        'hourly': generate_peak_hours_insight(hourly_pattern),
        'weekly': generate_weekly_pattern_insight(daily_pattern),
        'prediction': generate_prediction_insight(predictions)
    }
