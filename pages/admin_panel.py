import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import time

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
    
    # Advanced Settings Section
    with st.expander("⚙️ Advanced Settings", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            optimization_mode = st.selectbox(
                "Optimization Mode",
                ["Balanced", "Minimize Waiting Time", "Maximize Throughput", "Emergency Priority"]
            )
            learning_rate = st.slider("Learning Rate", 0.001, 0.1, 0.01, format="%.3f")
        with col2:
            update_frequency = st.selectbox(
                "Update Frequency",
                ["Real-time", "Every 5 minutes", "Every 15 minutes", "Every hour"]
            )
            prediction_horizon = st.slider("Prediction Horizon (hours)", 1, 24, 6)
    
    # Real-time Traffic Conditions
    st.subheader("🚦 Real-time Traffic Conditions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        traffic_density = st.slider("Current Traffic Density (%)", 0, 100, 50)
        st.metric("Current Flow Rate", "1250 vehicles/hour")
    
    with col2:
        queue_length = st.slider("Queue Length (vehicles)", 0, 50, 10)
        st.metric("Average Speed", "35 km/h")
    
    with col3:
        emergency_vehicles = st.number_input("Emergency Vehicles", 0, 10, 0)
        st.metric("Waiting Time", "45 seconds")

    # Peak Hours Configuration
    st.subheader("⏰ Peak Hours Configuration")
    morning_peak = st.slider(
        "Morning Peak Hours",
        value=(8, 10),
        min_value=0,
        max_value=12,
        format="%d:00"
    )
    evening_peak = st.slider(
        "Evening Peak Hours",
        value=(17, 19),
        min_value=12,
        max_value=23,
        format="%d:00"
    )
    
    # Intersection Priority
    st.subheader("🛣️ Intersection Priority")
    priorities = st.multiselect(
        "Select High Priority Intersections",
        ["Main Street - 1st Ave", "Downtown Junction", "Hospital Route", "School Zone", "Shopping District"],
        default=["Hospital Route", "School Zone"]
    )

    # AI Model Performance Metrics
    st.subheader("📊 AI Model Performance")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Accuracy", "94.5%", delta="1.2%")
    with col2:
        st.metric("Average Response Time", "0.8s", delta="-0.1s")
    with col3:
        st.metric("Optimization Score", "8.7/10", delta="0.5")

    # Optimization Action
    if st.button("🚀 Run AI Optimization", use_container_width=True):
        with st.spinner("Running AI optimization algorithm..."):
            # Calculate optimized timings based on all parameters
            progress_bar = st.progress(0)
            for i in range(100):
                # Simulate optimization progress
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            
            # Show Results
            st.success("✅ Signal timing optimization completed!")
            
            # Display Optimization Results
            st.subheader("🎯 Optimization Results")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Optimized Cycle Length", "120 seconds")
                st.metric("Green Time (Main)", "45 seconds")
                st.metric("Green Time (Cross)", "35 seconds")
                st.metric("Expected Delay Reduction", "25%")
            
            with col2:
                st.metric("Intersection Efficiency", "85%", delta="15%")
                st.metric("Queue Length Reduction", "30%")
                st.metric("Average Speed Improvement", "20%")
                st.metric("Estimated Travel Time Saving", "4.5 minutes")

            # Recommendations
            st.info("""
            **AI Recommendations:**
            1. Increase green time during morning peak (8:00-10:00)
            2. Implement dynamic timing for emergency vehicle priority
            3. Adjust cycle length based on real-time queue length
            4. Consider coordinated timing with adjacent intersections
            """)

with tab1:
    create_signal_controls()
    
with tab2:
    display_analytics()

with tab3:
    optimize_signals()
