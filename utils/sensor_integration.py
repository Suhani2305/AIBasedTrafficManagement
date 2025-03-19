
import requests
from typing import Dict, List
import json
import time

class SensorIntegration:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://traffic-sensors-api.example.com"  # Replace with real API
        self.sensors = {}

    def register_sensor(self, sensor_id: str, location: str, sensor_type: str):
        """Register a new traffic sensor"""
        self.sensors[sensor_id] = {
            'location': location,
            'type': sensor_type,
            'last_reading': None
        }

    def get_sensor_data(self, sensor_id: str) -> Dict:
        """Get real-time data from a specific sensor"""
        try:
            # In production, replace with real API call
            response = {
                'sensor_id': sensor_id,
                'timestamp': time.time(),
                'vehicle_count': 0,
                'average_speed': 0,
                'density': 0
            }
            
            # Example of real API call:
            # response = requests.get(
            #     f"{self.base_url}/sensors/{sensor_id}",
            #     headers={'Authorization': f'Bearer {self.api_key}'}
            # ).json()
            
            self.sensors[sensor_id]['last_reading'] = response
            return response
        except Exception as e:
            print(f"Error reading sensor {sensor_id}: {str(e)}")
            return None

    def get_all_sensors_data(self) -> List[Dict]:
        """Get data from all registered sensors"""
        return [
            self.get_sensor_data(sensor_id)
            for sensor_id in self.sensors.keys()
        ]
