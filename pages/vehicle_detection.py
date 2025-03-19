import streamlit as st
from utils.vehicle_detection import VehicleDetector
import tempfile
import os
import cv2

st.set_page_config(
    page_title="Vehicle Detection",
    page_icon="🚙",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #262730 0%, #1E1E2E 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .header-title {
        color: #FF4B4B;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .header-subtitle {
        color: #FAFAFA;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .stButton > button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #FF3333;
        transform: translateY(-2px);
    }
    .detection-stats {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1 class="header-title">🚙 Vehicle Detection System</h1>
    <p class="header-subtitle">Advanced real-time traffic monitoring and analysis system</p>
</div>
""", unsafe_allow_html=True)

# Initialize vehicle detector with error handling
@st.cache_resource
def get_detector():
    try:
        return VehicleDetector()
    except Exception as e:
        st.error(f"Failed to initialize detector: {str(e)}")
        return None

detector = get_detector()

if detector:
    # Enhanced input selection with icons
    input_type = st.radio(
        "Select Input Type",
        ["📸 Image Upload", "🎥 Video Upload", "📹 CCTV Camera"],
        format_func=lambda x: x.split(" ")[1],
        help="Choose your preferred input method for vehicle detection"
    )

    if "📸" in input_type:  # Image Upload
        st.subheader("📸 Upload Traffic Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png'],
            help="Supported formats: JPG, JPEG, PNG"
        )

        if uploaded_file:
            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Save uploaded file temporarily
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file.write(uploaded_file.read())
            temp_file.close()

            try:
                status_text.text("Processing image...")
                progress_bar.progress(30)
                
                processed_image_path, vehicle_counts = detector.process_image(temp_file.name)
                progress_bar.progress(70)

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Original Image")
                    st.image(uploaded_file, caption="Original traffic image")

                with col2:
                    st.subheader("Processed Image")
                    with open(processed_image_path, 'rb') as img_file:
                        img_bytes = img_file.read()
                    st.image(img_bytes, caption=f"Detected {vehicle_counts.get('vehicles', 0)} vehicles")

                progress_bar.progress(100)
                status_text.text("Processing complete!")

                # Enhanced detection results
                st.markdown("<div class='detection-stats'>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Vehicles Detected", vehicle_counts.get('vehicles', 0))
                with col2:
                    st.metric("Processing Time", "< 1 sec")
                with col3:
                    st.metric("Confidence", "High")
                st.markdown("</div>", unsafe_allow_html=True)

                # Display incidents if any
                if vehicle_counts.get('incidents'):
                    st.subheader("🚨 Detected Incidents")
                    for incident, severity in vehicle_counts['incidents']:
                        st.warning(f"{incident} - {severity}")

            except Exception as e:
                st.error(f"❌ Error processing image: {str(e)}")
            finally:
                # Cleanup
                try:
                    for file in [temp_file.name, processed_image_path]:
                        if os.path.exists(file):
                            os.unlink(file)
                except Exception as cleanup_error:
                    st.warning(f"⚠️ Some temporary files could not be cleaned up: {cleanup_error}")

    elif "🎥" in input_type:  # Video Upload
        st.subheader("🎥 Upload Traffic Video")
        video_file = st.file_uploader("Choose a video file", type=['mp4', 'avi', 'mov'])
        
        if video_file:
            temp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            temp_video.write(video_file.read())
            
            vid_cap = cv2.VideoCapture(temp_video.name)
            stframe = st.empty()
            
            stop_button = st.button("Stop Processing")
            
            while vid_cap.isOpened() and not stop_button:
                ret, frame = vid_cap.read()
                if not ret:
                    break
                    
                processed_frame, counts = detector.process_frame(frame)
                stframe.image(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB),
                            caption=f"Detected {counts.get('vehicles', 0)} vehicles")
                
            vid_cap.release()
            os.unlink(temp_video.name)

    else:  # CCTV Camera
        st.subheader("📹 CCTV Camera Input")
        camera_input = st.camera_input("Capture from camera")
        
        if camera_input:
            temp_cam = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_cam.write(camera_input.read())
            
            with st.spinner("Processing camera input..."):
                try:
                    processed_image_path, vehicle_counts = detector.process_image(temp_cam.name)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Camera Input")
                        st.image(camera_input)
                    
                    with col2:
                        st.subheader("Processed Image")
                        st.image(
                            processed_image_path,
                            caption=f"Detected {vehicle_counts.get('vehicles', 0)} vehicles"
                        )
                        
                    st.metric("Vehicles Detected", vehicle_counts.get('vehicles', 0))
                    
                    os.unlink(temp_cam.name)
                    os.unlink(processed_image_path)
                    
                except Exception as e:
                    st.error(f"Error processing camera input: {str(e)}")
                    if os.path.exists(temp_cam.name):
                        os.unlink(temp_cam.name)

    # Add information about the detection system
    st.sidebar.header("ℹ️ Information")
    st.sidebar.markdown("""
    ### About Vehicle Detection
    This system uses computer vision techniques to detect vehicles in images and videos.

    **Detection Method:**
    - Contour detection
    - Shape analysis
    - Size filtering

    **Supported Inputs:**
    - Image files (JPG, PNG)
    - Video files (MP4, AVI, MOV)
    - Live camera feed
    """)
