
import streamlit as st
from datetime import datetime
import random

class EmergencyResponseSystem:
    def __init__(self):
        self.emergency_services = {
            'ambulance': {'count': 5, 'response_time': '4-6'},
            'police': {'count': 8, 'response_time': '5-7'},
            'fire': {'count': 3, 'response_time': '6-8'}
        }
    
    def dispatch_emergency_service(self, service_type, location):
        return {
            'unit_id': f"{service_type[:3].upper()}-{random.randint(100,999)}",
            'dispatch_time': datetime.now().strftime("%H:%M:%S"),
            'est_arrival': f"{random.randint(4,8)} minutes"
        }
        
    def get_available_units(self):
        return {k: v['count'] for k, v in self.emergency_services.items()}
