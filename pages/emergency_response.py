
import streamlit as st
from utils.emergency import EmergencyResponseSystem
from datetime import datetime

st.set_page_config(page_title="Emergency Response", page_icon="🚨", layout="wide")

st.markdown("""
<div style='text-align: center; background-color: #262730; padding: 2rem; border-radius: 10px; margin-bottom: 2rem'>
    <h1 style='color: #FF4B4B'>🚨 Emergency Response System</h1>
    <p style='color: #FAFAFA; font-size: 1.2rem'>Rapid Response Management</p>
</div>
""", unsafe_allow_html=True)

ers = EmergencyResponseSystem()

col1, col2 = st.columns([2,1])

with col1:
    st.subheader("🚑 Emergency Dispatch")
    
    emergency_type = st.selectbox(
        "Emergency Type",
        ["Medical Emergency", "Traffic Accident", "Fire", "Police Assistance"]
    )
    
    location = st.text_input("Location", "")
    
    if st.button("Dispatch Emergency Services"):
        if location:
            response = ers.dispatch_emergency_service('ambulance', location)
            st.success(f"Emergency unit {response['unit_id']} dispatched!")
            st.info(f"Estimated arrival time: {response['est_arrival']}")
        else:
            st.error("Please enter a location")

with col2:
    st.subheader("📍 Available Units")
    units = ers.get_available_units()
    for service, count in units.items():
        st.metric(f"{service.title()} Units", count)
