import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from utils.data_generator import generate_mock_traffic_data
from utils.analysis import calculate_statistics, analyze_patterns
from utils.prediction import train_prediction_model, predict_next_day
from utils.insights import get_all_insights
from utils.data_collector import scrape_traffic_data, get_sensor_data, process_traffic_updates
from fastapi import FastAPI # Added import for FastAPI


# Placeholder functions for mobile app and sensor/camera integration
class CameraManager:
    def __init__(self):
        self.cameras = {}

    def add_camera(self, name, url, location):
        self.cameras[name] = {"url": url, "location": location, "stream": None}

    def start_camera(self, name):
        # Placeholder: Replace with actual camera stream processing
        self.cameras[name]["stream"] = "Streaming..."
        print(f"Camera {name} started (placeholder)")

class SensorIntegration:
    def __init__(self):
        self.sensors = {}

    def register_sensor(self, name, location, sensor_type):
        self.sensors[name] = {"location": location, "type": sensor_type, "data": []}

    def get_sensor_data(self, sensor_name):
        # Placeholder: Replace with actual sensor data retrieval
        return {"timestamp": datetime.now(), "value": 100}


async def mobile_app(request):
    #Placeholder: This needs to be the actual mobile app implementation using FastAPI
    return {"message": "Mobile app endpoint (placeholder)"}


# Page configuration
st.set_page_config(
    page_title="Traffic Analysis Dashboard",
    page_icon="🚗",
    layout="wide"
)

# Navbar with title
st.markdown("""
<nav style='background-color: #FF4B4B; padding: 1rem; position: fixed; top: 0; left: 0; right: 0; z-index: 999'>
    <h1 style='color: white; margin: 0; text-align: center; font-size: 2rem'>🚗 IntelliRoute</h1>
</nav>
<div style='margin-top: 5rem'>
    <div style='text-align: center; background-color: #262730; padding: 2rem; border-radius: 10px; margin-bottom: 2rem'>
        <h2 style='color: #FF4B4B'>Smart Traffic Analysis Dashboard</h2>
        <p style='color: #FAFAFA; font-size: 1.2rem'>Real-time traffic monitoring and analytics platform</p>
    </div>
</div>
""", unsafe_allow_html=True)



# City selection
selected_city = st.sidebar.selectbox(
    "Select City",
    ["Bangalore", "Mumbai", "Delhi", "Chennai"],
    key="city_selector"
)

# Real-time Traffic Status
st.header("🔴 Real-time Traffic Status")
traffic_status = scrape_traffic_data(selected_city)

# Display current traffic status
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Congestion Level",
        f"{traffic_status['congestion_level']}%",
        delta="5%"
    )

with col2:
    st.metric(
        "Affected Areas",
        len(traffic_status['affected_areas'])
    )

with col3:
    st.metric(
        "Active Incidents",
        len(traffic_status['incidents'])
    )

# Display incidents in an expander
with st.expander("🚨 Traffic Incidents", expanded=True):
    for incident in traffic_status['incidents']:
        st.warning(
            f"**{incident['location']}**: {incident['type']} (Severity: {incident['severity']})"
        )

# Sensor Data Analysis
st.header("📊 Sensor Data Analysis")

# Time filter
st.sidebar.header("🕒 Time Filter")
selected_days = st.sidebar.slider(
    "Select number of days to analyze",
    min_value=1,
    max_value=30,
    value=7,
    key="time_filter"
)

sensor_data = get_sensor_data(selected_days)
traffic_insights = process_traffic_updates(sensor_data)

# Display sensor insights
col1, col2 = st.columns(2)
with col1:
    st.metric(
        "Average Speed",
        f"{traffic_insights['average_speed']:.1f} km/h"
    )
    st.metric(
        "Total Vehicles",
        f"{traffic_insights['total_vehicles']:,}"
    )

with col2:
    st.metric(
        "Congestion Score",
        f"{traffic_insights['congestion_score']:.2f}"
    )
    st.metric(
        "Most Congested Area",
        traffic_insights['peak_volume_segment']
    )


# Sidebar - Chart Preferences
st.sidebar.header("📊 Chart Preferences")

# Color scheme selection
color_scheme = st.sidebar.selectbox(
    "Select Color Scheme",
    options=["Default", "Blues", "Reds", "Greens", "Purples"],
    key="color_scheme"
)

# Chart type for time series
timeline_chart_type = st.sidebar.radio(
    "Timeline Chart Type",
    options=["Line", "Bar"],
    key="timeline_type"
)

# Chart size
chart_height = st.sidebar.slider(
    "Chart Height (pixels)",
    min_value=300,
    max_value=800,
    value=400,
    step=50,
    key="chart_height"
)



# Generate data
@st.cache_data
def load_data():
    return generate_mock_traffic_data(days=30)

df = load_data()
filtered_df = df.iloc[-selected_days*24:]

# Calculate patterns and predictions
hourly_pattern, daily_pattern = analyze_patterns(filtered_df)
model, train_score, test_score = train_prediction_model(df)
predictions = predict_next_day(model, df)

# Generate insights
insights = get_all_insights(filtered_df, hourly_pattern, daily_pattern, predictions)

# Display key metrics with insights
st.header("📊 Key Traffic Metrics")
stats = calculate_statistics(filtered_df)

# Add trend insight in an expandable section
with st.expander("🔍 Traffic Trend Analysis", expanded=True):
    st.info(insights['trend'])

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Average Daily Volume", f"{stats['avg_volume']:,.0f}")
with col2:
    st.metric("Peak Volume", f"{stats['peak_volume']:,.0f}")
with col3:
    st.metric("Minimum Volume", f"{stats['min_volume']:,.0f}")
with col4:
    st.metric("Standard Deviation", f"{stats['std_dev']:,.0f}")

# Get color based on scheme
def get_color_sequence(scheme):
    if scheme == "Default":
        return None
    else:
        return [scheme.lower()]

# Traffic Volume Over Time
st.header("📈 Traffic Volume Trends")

# Create timeline chart based on user preference
if timeline_chart_type == "Line":
    fig_timeline = px.line(
        filtered_df,
        x='timestamp',
        y='traffic_volume',
        title='Traffic Volume Over Time',
        color_discrete_sequence=get_color_sequence(color_scheme)
    )
else:
    fig_timeline = px.bar(
        filtered_df,
        x='timestamp',
        y='traffic_volume',
        title='Traffic Volume Over Time',
        color_discrete_sequence=get_color_sequence(color_scheme)
    )

# Update chart size
fig_timeline.update_layout(height=chart_height)
st.plotly_chart(fig_timeline, use_container_width=True)

# Pattern Analysis with insights
st.header("🔍 Traffic Patterns")

# Add hourly insights in an expandable section
with st.expander("📊 Hourly Traffic Insights", expanded=True):
    st.info(insights['hourly'])

col1, col2 = st.columns(2)

with col1:
    # Hourly patterns
    fig_hourly = px.bar(
        x=hourly_pattern.index,
        y=hourly_pattern.values,
        title='Average Traffic by Hour',
        labels={'x': 'Hour of Day', 'y': 'Average Traffic Volume'},
        color_discrete_sequence=get_color_sequence(color_scheme)
    )
    fig_hourly.update_layout(height=chart_height)
    st.plotly_chart(fig_hourly, use_container_width=True)

with col2:
    # Add weekly insights in an expandable section
    with st.expander("📅 Weekly Traffic Insights", expanded=True):
        st.info(insights['weekly'])

    # Daily patterns
    fig_daily = px.bar(
        x=daily_pattern.index,
        y=daily_pattern.values,
        title='Average Traffic by Day of Week',
        labels={'x': 'Day of Week', 'y': 'Average Traffic Volume'},
        color_discrete_sequence=get_color_sequence(color_scheme)
    )
    fig_daily.update_layout(height=chart_height)
    st.plotly_chart(fig_daily, use_container_width=True)

# Traffic Prediction with insights
st.header("🔮 Traffic Prediction")

# Add prediction insights in an expandable section
with st.expander("🎯 Prediction Insights", expanded=True):
    st.info(insights['prediction'])

# Display model performance
col1, col2 = st.columns(2)
with col1:
    st.metric("Training Score", f"{train_score:.2%}")
with col2:
    st.metric("Testing Score", f"{test_score:.2%}")

# Plot predictions
fig_pred = go.Figure()
fig_pred.add_trace(go.Scatter(
    x=list(range(24)),
    y=predictions,
    mode='lines+markers',
    name='Predicted Traffic',
    line=dict(color=color_scheme.lower()) if color_scheme != "Default" else dict()
))
fig_pred.update_layout(
    title='Predicted Traffic Volume for Next 24 Hours',
    xaxis_title='Hour of Day',
    yaxis_title='Predicted Traffic Volume',
    height=chart_height
)
st.plotly_chart(fig_pred, use_container_width=True)

# Footer with last update time
st.markdown("---")
st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
st.markdown("*Note: This dashboard uses mock data for demonstration purposes.*")

# Initialize and display notifications
from utils.notification import NotificationSystem
notifier = NotificationSystem()

# Example notifications
if len(traffic_status['incidents']) > 0:
    for incident in traffic_status['incidents']:
        notifier.add_notification(
            f"Traffic incident detected at {incident['location']}", 
            "warning"
        )

# Display notifications in sidebar
notifier.display_notifications()

# Initialize camera system
camera_manager = CameraManager()
camera_manager.add_camera("cam1", "rtsp://camera1.example.com/stream", "MG Road")
camera_manager.add_camera("cam2", "rtsp://camera2.example.com/stream", "Outer Ring Road")

# Initialize sensor integration
sensor_system = SensorIntegration()
sensor_system.register_sensor("sensor1", "MG Road", "vehicle_counter")
sensor_system.register_sensor("sensor2", "Outer Ring Road", "speed_detector")

# Placeholder main function (replace with actual main logic)
def main():
    print("Main function placeholder")

if __name__ == "__main__":
    # Start camera processing
    camera_manager.start_camera("cam1")
    camera_manager.start_camera("cam2")

    # Mount FastAPI app for mobile integration
    app = FastAPI()
    app.mount("/mobile", mobile_app)

    main()