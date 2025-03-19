import pandas as pd
import numpy as np

def calculate_statistics(df):
    """Calculate basic traffic statistics."""
    stats = {
        'total_volume': int(df['traffic_volume'].sum()),
        'avg_volume': round(df['traffic_volume'].mean(), 2),
        'peak_volume': int(df['traffic_volume'].max()),
        'min_volume': int(df['traffic_volume'].min()),
        'std_dev': round(df['traffic_volume'].std(), 2)
    }
    return stats

def analyze_patterns(df):
    """Analyze traffic patterns by time periods."""
    # Hourly patterns
    hourly_pattern = df.groupby('hour')['traffic_volume'].mean().round(2)
    
    # Daily patterns
    daily_pattern = df.groupby('day_of_week')['traffic_volume'].mean().round(2)
    
    return hourly_pattern, daily_pattern
