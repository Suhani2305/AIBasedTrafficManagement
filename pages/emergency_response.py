import streamlit as st
import time
from datetime import datetime, timedelta
import random

# Custom CSS for better styling
st.markdown("""
<style>
    .emergency-header {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF0000 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.2);
    }
    .status-active {
        color: #00FF00;
        font-weight: bold;
    }
    .status-enroute {
        color: #FFA500;
        font-weight: bold;
    }
    .status-completed {
        color: #808080;
    }
    .emergency-card {
        background-color: #2C3333;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #FF4B4B;
    }
    .metric-card {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    .dispatch-form {
        background-color: #2C3333;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 1rem;
    }
    .team-card {
        background-color: #2C3333;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        border-left: 4px solid #00FF00;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class='emergency-header'>
    <h1 style='color: white; text-align: center; font-size: 2.5rem;'>🚨 Emergency Response System</h1>
    <p style='color: white; text-align: center; font-size: 1.2rem;'>Real-time Emergency Management & Response</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for emergency cases
if 'emergency_cases' not in st.session_state:
    st.session_state.emergency_cases = [
        {
            'id': 'EM001',
            'type': 'Traffic Accident',
            'location': 'MG Road - Brigade Junction',
            'status': 'Active',
            'time': datetime.now() - timedelta(minutes=5),
            'severity': 'High',
            'units_assigned': ['AMB-102', 'POL-205'],
            'eta': '3 minutes'
        },
        {
            'id': 'EM002',
            'type': 'Vehicle Breakdown',
            'location': 'Electronic City Flyover',
            'status': 'En Route',
            'time': datetime.now() - timedelta(minutes=15),
            'severity': 'Medium',
            'units_assigned': ['TOW-103'],
            'eta': '8 minutes'
        }
    ]

# Main content area with tabs
tab1, tab2, tab3 = st.tabs(["📍 Active Emergencies", "🚑 Response Teams", "📊 Analytics"])

with tab1:
    # Emergency Dispatch Form
    st.markdown("### 🆘 Emergency Dispatch")
    with st.container():
        st.markdown("<div class='dispatch-form'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            emergency_type = st.selectbox(
                "Emergency Type",
                ["Traffic Accident", "Medical Emergency", "Vehicle Breakdown", 
                 "Fire Incident", "Police Assistance", "Hazardous Situation"]
            )
            location = st.text_input("Location", placeholder="Enter incident location")
            severity = st.select_slider(
                "Severity Level",
                options=["Low", "Medium", "High", "Critical"],
                value="Medium"
            )
        
        with col2:
            additional_info = st.text_area("Additional Information", placeholder="Describe the emergency situation...")
            units_needed = st.multiselect(
                "Required Units",
                ["Ambulance", "Police", "Fire Engine", "Tow Truck", "Hazmat Team"],
                default=["Ambulance"] if emergency_type == "Medical Emergency" else ["Police"]
            )
        
        if st.button("🚨 DISPATCH EMERGENCY RESPONSE", use_container_width=True):
            if location:
                with st.spinner("Dispatching emergency response units..."):
                    # Simulate dispatch process
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    # Add new emergency case
                    new_case = {
                        'id': f'EM{len(st.session_state.emergency_cases) + 1:03d}',
                        'type': emergency_type,
                        'location': location,
                        'status': 'Active',
                        'time': datetime.now(),
                        'severity': severity,
                        'units_assigned': [f"{unit[:3].upper()}-{random.randint(100,999)}" for unit in units_needed],
                        'eta': f"{random.randint(2,15)} minutes"
                    }
                    st.session_state.emergency_cases.insert(0, new_case)
                    st.success("✅ Emergency response units dispatched successfully!")
            else:
                st.error("Please enter the incident location!")
        st.markdown("</div>", unsafe_allow_html=True)

    # Active Emergency Cases
    st.markdown("### 🎯 Active Emergency Cases")
    for case in st.session_state.emergency_cases:
        st.markdown(f"""
        <div class='emergency-card'>
            <h3 style='color: #FF4B4B;'>{case['type']} - {case['id']}</h3>
            <p><strong>Location:</strong> {case['location']}</p>
            <p><strong>Status:</strong> <span class='status-{case['status'].lower().replace(" ", "")}'>{case['status']}</span></p>
            <p><strong>Time Reported:</strong> {case['time'].strftime('%I:%M %p')}</p>
            <p><strong>Severity:</strong> {case['severity']}</p>
            <p><strong>Units Assigned:</strong> {', '.join(case['units_assigned'])}</p>
            <p><strong>ETA:</strong> {case['eta']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    # Response Teams Management
    st.markdown("### 👥 Available Response Teams")
    
    # Team Status Overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Ambulances", "8/10", "2 Dispatched")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Police Units", "12/15", "3 Dispatched")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Fire Engines", "5/5", "All Available")
        st.markdown("</div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Tow Trucks", "3/4", "1 Dispatched")
        st.markdown("</div>", unsafe_allow_html=True)

    # Team Details
    teams = [
        {"id": "AMB-101", "type": "Ambulance", "status": "Available", "location": "City Hospital", "last_active": "10 mins ago"},
        {"id": "POL-204", "type": "Police", "status": "En Route", "location": "MG Road", "last_active": "Active Now"},
        {"id": "FIR-103", "type": "Fire Engine", "status": "Available", "location": "Central Station", "last_active": "1 hour ago"},
        {"id": "TOW-102", "type": "Tow Truck", "status": "Available", "location": "Service Center", "last_active": "30 mins ago"}
    ]

    for team in teams:
        st.markdown(f"""
        <div class='team-card'>
            <h4>{team['id']} - {team['type']}</h4>
            <p><strong>Status:</strong> <span class='status-{team['status'].lower().replace(" ", "")}'>{team['status']}</span></p>
            <p><strong>Current Location:</strong> {team['location']}</p>
            <p><strong>Last Active:</strong> {team['last_active']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    # Response Analytics
    st.markdown("### 📊 Emergency Response Analytics")
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Average Response Time", "4.5 mins", "-30s")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Cases Today", "15", "+3")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Resolution Rate", "94%", "+2%")
        st.markdown("</div>", unsafe_allow_html=True)

    # Response Time Distribution
    st.markdown("#### ⏱️ Response Time Distribution")
    response_times = {
        "< 5 mins": 45,
        "5-10 mins": 30,
        "10-15 mins": 15,
        "15+ mins": 10
    }
    
    # Create a simple bar chart
    st.bar_chart(response_times)

    # Recent Performance
    st.markdown("#### 📈 Recent Performance")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Critical Cases Handled", "8/8", "100%")
        st.metric("Team Availability", "85%", "+5%")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Resource Utilization", "78%", "Optimal")
        st.metric("Coordination Score", "9.2/10", "+0.3")
        st.markdown("</div>", unsafe_allow_html=True)

# Footer with real-time updates
st.markdown("---")
st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
