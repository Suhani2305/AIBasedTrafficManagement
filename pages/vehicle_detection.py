
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

st.markdown("""
<div style='text-align: center; background-color: #262730; padding: 2rem; border-radius: 10px; margin-bottom: 2rem'>
    <h1 style='color: #FF4B4B'>🚙 Vehicle Detection System</h1>
    <p style='color: #FAFAFA; font-size: 1.2rem'>Advanced real-time traffic monitoring and analysis system</p>
</div>
""", unsafe_allow_html=True)



# Initialize vehicle detector
@st.cache_resource
def get_detector():
    return VehicleDetector()

try:
    detector = get_detector()

    # Input selection
    input_type = st.radio(
        "Select Input Type",
        ["Image Upload", "Video Upload", "CCTV Camera"],
        help="Choose your preferred input method"
    )

    if input_type == "Image Upload":
        # File uploader for images
        st.subheader("Upload Traffic Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a traffic image to detect vehicles"
        )

        if uploaded_file:
            # Save uploaded file temporarily
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file.write(uploaded_file.read())

            with st.spinner("Processing image..."):
                try:
                    # Process image
                    processed_image_path, vehicle_counts = detector.process_image(temp_file.name)

                    # Display results
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Original Image")
                        st.image(uploaded_file, caption="Original traffic image")

                    with col2:
                        st.subheader("Processed Image")
                        st.image(
                            processed_image_path,
                            caption=f"Detected {vehicle_counts.get('vehicles', 0)} vehicles"
                        )

                    # Display vehicle counts
                    st.subheader("Detection Results")
                    st.metric(
                        "Vehicles Detected",
                        vehicle_counts.get('vehicles', 0),
                        help="Total number of vehicles detected in the image"
                    )

                    # Cleanup temporary files
                    os.unlink(temp_file.name)
                    os.unlink(processed_image_path)

                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")
                    if os.path.exists(temp_file.name):
                        os.unlink(temp_file.name)

    elif input_type == "Video Upload":
        st.subheader("Upload Traffic Video")
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
        st.subheader("CCTV Camera Input")
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

except Exception as e:
    st.error(f"Error initializing vehicle detector: {str(e)}")
