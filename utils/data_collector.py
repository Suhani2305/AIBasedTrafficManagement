import trafilatura
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List

def scrape_traffic_data(city: str) -> Dict:
    """
    Scrape traffic data from various sources for a given city.
    Currently uses mock data, but can be extended to use real APIs.
    """
    # Mock data structure similar to what we'd get from real sources
    traffic_status = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'city': city,
        'congestion_level': 75,  # percentage
        'affected_areas': ['MG Road', 'Outer Ring Road', 'Electronic City'],
        'incidents': [
            {'location': 'MG Road', 'type': 'Heavy Traffic', 'severity': 'High'},
            {'location': 'Outer Ring Road', 'type': 'Construction', 'severity': 'Medium'}
        ]
    }
    return traffic_status

def get_sensor_data(days=7) -> pd.DataFrame:
    """
    Simulate sensor data collection from traffic sensors.
    In production, this would connect to real sensors via APIs.
    """
    current_time = datetime.now()
    times = [current_time - timedelta(hours=i) for i in range(days * 24)]
    
    # Generate more realistic data based on time patterns
    data = []
    for t in times:
        hour = t.hour
        # Simulate peak hours
        multiplier = 1.5 if (8 <= hour <= 10) or (16 <= hour <= 18) else 1.0
        
        for sensor in ['S1', 'S2', 'S3']:
            data.append({
                'timestamp': t,
                'sensor_id': sensor,
                'vehicle_count': int(np.random.normal(100, 20) * multiplier),
                'average_speed': max(20, min(60, np.random.normal(40, 10))),
                'road_segment': {'S1': 'MG Road', 'S2': 'Outer Ring Road', 'S3': 'Electronic City'}[sensor]
            })
    
    data = pd.DataFrame(data)
    
    return data

def process_traffic_updates(data: pd.DataFrame) -> Dict[str, float]:
    """
    Process and analyze traffic updates to extract meaningful insights.
    """
    insights = {
        'average_speed': data['average_speed'].mean(),
        'total_vehicles': data['vehicle_count'].sum(),
        'congestion_score': calculate_congestion_score(data),
        'peak_volume_segment': data.groupby('road_segment')['vehicle_count'].mean().idxmax()
    }
    return insights

def calculate_congestion_score(data: pd.DataFrame) -> float:
    """
    Calculate a congestion score based on vehicle count and average speed.
    Returns a value between 0 (no congestion) and 1 (severe congestion).
    """
    # Normalize vehicle count and speed (inverse)
    max_count = data['vehicle_count'].max()
    norm_count = data['vehicle_count'] / max_count
    
    min_speed = data['average_speed'].min()
    max_speed = data['average_speed'].max()
    norm_speed = 1 - (data['average_speed'] - min_speed) / (max_speed - min_speed)
    
    # Combine into a single score
    congestion_score = (norm_count * 0.6 + norm_speed * 0.4).mean()
    return round(congestion_score, 2)
