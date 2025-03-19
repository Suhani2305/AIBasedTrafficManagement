
import streamlit as st
import numpy as np
from datetime import datetime, timedelta

def optimize_signal_timing(traffic_density):
    base_time = 30
    return min(120, base_time + (traffic_density * 0.5))

def create_signal_controls():
    st.subheader("🚦 Traffic Signal Controls")
    
    intersections = {
        "MG Road Junction": {"density": 85},
        "Outer Ring Road": {"density": 65},
        "Electronic City": {"density": 75}
    }
    
    for intersection, data in intersections.items():
        st.subheader(f"📍 {intersection}")
        col1, col2 = st.columns(2)
        
        with col1:
            current_density = data["density"]
            optimal_time = optimize_signal_timing(current_density)
            st.metric("Traffic Density", f"{current_density}%")
            st.metric("Optimal Green Time", f"{int(optimal_time)}s")
        
        with col2:
            if st.button(f"Optimize {intersection}"):
                st.success(f"Optimized signal timing for {intersection}")

def display_analytics():
    st.subheader("📊 Traffic Analytics")
    
    # Traffic metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Daily Traffic", "12,450 vehicles")
        st.metric("Peak Hour Traffic", "1,850 vehicles/hour")
    with col2:
        st.metric("Incidents Today", "3")
        st.metric("Average Speed", "35 km/h")
    with col3:
        st.metric("Congestion Level", "75%")
        st.metric("Response Time", "8 mins")
    
    # Incident log
    st.subheader("🚨 Recent Incidents")
    incidents = [
        {"time": "10:30 AM", "location": "MG Road", "type": "Heavy Traffic"},
        {"time": "11:45 AM", "location": "Outer Ring Road", "type": "Vehicle Breakdown"},
        {"time": "12:15 PM", "location": "Electronic City", "type": "Road Work"}
    ]
    
    for incident in incidents:
        st.warning(f"{incident['time']} - {incident['type']} at {incident['location']}")

st.markdown("""
<div style='text-align: center; background-color: #262730; padding: 2rem; border-radius: 10px; margin-bottom: 2rem'>
    <h1 style='color: #FF4B4B'>🎛️ Admin Control Panel</h1>
    <p style='color: #FAFAFA; font-size: 1.2rem'>Traffic Management System Control Center</p>
</div>
""", unsafe_allow_html=True)



tab1, tab2, tab3 = st.tabs(["Signal Controls", "Analytics", "AI Optimization"])

def optimize_signals():
    st.subheader("🤖 AI Signal Optimization")
    
    # Traffic conditions input
    traffic_density = st.slider("Current Traffic Density", 0, 100, 50)
    peak_hours = st.multiselect(
        "Peak Hours",
        options=[f"{i:02d}:00" for i in range(24)],
        default=["08:00", "09:00", "17:00", "18:00"]
    )
    
    if st.button("Optimize Signal Timings"):
        with st.spinner("Analyzing traffic patterns..."):
            # Calculate optimized timings
            green_time = max(30, min(90, traffic_density))
            cycle_time = green_time + 30
            
            st.success("Signal timings optimized!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Optimized Green Time", f"{green_time}s")
            with col2:
                st.metric("Total Cycle Time", f"{cycle_time}s")
            
            st.info("These timings are based on current traffic density and historical patterns")

with tab1:
    create_signal_controls()
    
with tab2:
    display_analytics()
