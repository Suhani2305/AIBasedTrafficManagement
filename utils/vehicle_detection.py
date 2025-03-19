
import cv2
import numpy as np
from typing import Dict, Tuple
import tempfile

import cv2
import numpy as np
from typing import Dict, Tuple
import tempfile

class VehicleDetector:
    def __init__(self):
        self.min_area = 500
        self.blur_size = (5, 5)  # Gaussian blur kernel size
        self.vehicle_types = {
            'small': (500, 2000),    # bikes, small cars
            'medium': (2000, 5000),  # cars, vans
            'large': (5000, 15000)   # trucks, buses
        }
        self.incident_threshold = 0.8  # threshold for incident detection
        self.prev_centroids = []  # Store previous frame centroids
        self.movement_threshold = 10  # Minimum pixels to consider movement

    def classify_vehicle(self, area):
        for v_type, (min_a, max_a) in self.vehicle_types.items():
            if min_a <= area < max_a:
                return v_type
        return 'unknown'

    def detect_incidents(self, frame, contours):
        incidents = []
        
        # Calculate density metrics
        density = len([c for c in contours if cv2.contourArea(c) > self.min_area])
        total_area = sum(cv2.contourArea(c) for c in contours if cv2.contourArea(c) > self.min_area)
        avg_area = total_area / len(contours) if contours else 0
        
        # Detect various incidents
        if density > 10:
            incidents.append(("High Traffic Density", "Warning"))
            
        if avg_area > 6000:
            incidents.append(("Traffic Congestion", "Alert"))
            
        # Detect stopped vehicles
        for contour in contours:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w)/h
            
            if area > 8000 and 0.8 <= aspect_ratio <= 1.2:
                incidents.append(("Possible Stopped Vehicle", "Alert"))
            elif area > 12000:
                incidents.append(("Large Vehicle Blockage", "Warning"))
                
        # Detect unusual patterns
        if density > 15 and avg_area < 1000:
            incidents.append(("Unusual Traffic Pattern", "Warning"))
            
        return incidents

    def __init__(self):
        self.min_area = 500
        self.blur_size = (5, 5)
        self.vehicle_types = {
            'small': (500, 2000),    # bikes, small cars
            'medium': (2000, 5000),  # cars, vans
            'large': (5000, 15000)   # trucks, buses
        }
        self.incident_threshold = 0.8
        self.prev_centroids = []  # Store previous frame centroids
        self.movement_threshold = 10  # Minimum pixels to consider movement

    def detect_movement(self, current_centroids):
        movements = []
        if self.prev_centroids:
            for curr in current_centroids:
                for prev in self.prev_centroids:
                    if abs(curr[1] - prev[1]) < 50:  # Same vertical region
                        if curr[0] - prev[0] > self.movement_threshold:
                            movements.append('right')
                        elif prev[0] - curr[0] > self.movement_threshold:
                            movements.append('left')
        self.prev_centroids = current_centroids
        return movements

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict[str, int]]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, self.blur_size, 0)
        thresh = cv2.adaptiveThreshold(
            blurred, 
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2
        )
        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        vehicle_count = 0
        current_centroids = []
        incidents = self.detect_incidents(frame, contours)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_area:
                vehicle_count += 1
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                v_type = self.classify_vehicle(area)
                # Calculate centroid
                cx = x + w//2
                cy = y + h//2
                current_centroids.append((cx, cy))
                
                # Draw centroid and vehicle info
                cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
                movements = self.detect_movement(current_centroids)
                movement_dir = 'left' if 'left' in movements else 'right' if 'right' in movements else 'stationary'
                
                cv2.putText(
                    frame,
                    f'Vehicle ({v_type}) - {movement_dir}',
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

        for incident, severity in incidents:
            cv2.putText(frame, f"{incident} - {severity}", (10, 30 + len(incidents) * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,0,255),2)

        return frame, {'vehicles': vehicle_count, 'incidents': incidents}

    def process_image(self, image_path: str) -> Tuple[str, Dict[str, int]]:
        frame = cv2.imread(image_path)
        if frame is None:
            raise ValueError("Failed to load image. Please ensure the image is valid.")

        processed_frame, counts = self.process_frame(frame)
        temp_output = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        cv2.imwrite(temp_output.name, processed_frame)
        return temp_output.name, counts