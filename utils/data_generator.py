import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_mock_traffic_data(days=30):
    """Generate mock traffic data for analysis."""
    np.random.seed(42)
    
    # Generate timestamps
    base = datetime.now() - timedelta(days=days)
    timestamps = [base + timedelta(hours=x) for x in range(days * 24)]
    
    # Generate traffic volumes with daily and weekly patterns
    traffic_volume = []
    for ts in timestamps:
        # Base volume
        base_volume = 500
        
        # Daily pattern (peak hours)
        hour_factor = 1.0
        if 7 <= ts.hour <= 9:  # Morning peak
            hour_factor = 2.0
        elif 16 <= ts.hour <= 18:  # Evening peak
            hour_factor = 1.8
        elif 0 <= ts.hour <= 5:  # Night hours
            hour_factor = 0.3
            
        # Weekly pattern
        week_factor = 0.7 if ts.weekday() >= 5 else 1.0  # Weekend vs Weekday
        
        # Calculate final volume with some random variation
        volume = base_volume * hour_factor * week_factor * np.random.normal(1, 0.1)
        traffic_volume.append(int(max(0, volume)))
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'traffic_volume': traffic_volume,
        'day_of_week': [ts.strftime('%A') for ts in timestamps],
        'hour': [ts.hour for ts in timestamps]
    })
    
    return df
