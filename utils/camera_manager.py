
import cv2
from typing import Dict, List
import threading
import queue
import numpy as np

class CameraManager:
    def __init__(self):
        self._cameras: Dict[str, dict] = {}
        self._frames: Dict[str, queue.Queue] = {}
        self._active_threads: Dict[str, threading.Thread] = {}

    def add_camera(self, camera_id: str, url: str, location: str):
        """Add a new camera feed"""
        if camera_id not in self._cameras:
            self._cameras[camera_id] = {
                'url': url,
                'location': location,
                'active': False
            }
            self._frames[camera_id] = queue.Queue(maxsize=10)

    def start_camera(self, camera_id: str):
        """Start processing a camera feed"""
        if camera_id in self._cameras and not self._cameras[camera_id]['active']:
            thread = threading.Thread(
                target=self._process_camera_feed,
                args=(camera_id,),
                daemon=True
            )
            thread.start()
            self._active_threads[camera_id] = thread
            self._cameras[camera_id]['active'] = True

    def _process_camera_feed(self, camera_id: str):
        """Process individual camera feed"""
        cap = cv2.VideoCapture(self._cameras[camera_id]['url'])
        while self._cameras[camera_id]['active']:
            ret, frame = cap.read()
            if ret:
                if self._frames[camera_id].full():
                    self._frames[camera_id].get()
                self._frames[camera_id].put(frame)
        cap.release()

    def get_frame(self, camera_id: str) -> np.ndarray:
        """Get latest frame from a camera"""
        if camera_id in self._frames and not self._frames[camera_id].empty():
            return self._frames[camera_id].get()
        return None

    def stop_camera(self, camera_id: str):
        """Stop processing a camera feed"""
        if camera_id in self._cameras:
            self._cameras[camera_id]['active'] = False
            if camera_id in self._active_threads:
                self._active_threads[camera_id].join()

def get_active_cameras():
    """Get list of active cameras"""
    camera_manager = CameraManager()
    return [
        {"id": cam_id, "location": cam_info["location"]}
        for cam_id, cam_info in camera_manager._cameras.items()
        if cam_info["active"]
    ]
