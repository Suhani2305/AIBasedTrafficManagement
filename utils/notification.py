
from datetime import datetime
import streamlit as st

class NotificationSystem:
    def __init__(self):
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
    
    def add_notification(self, message, level="info"):
        notification = {
            "message": message,
            "level": level,
            "timestamp": datetime.now()
        }
        st.session_state.notifications.append(notification)
    
    def display_notifications(self):
        if st.session_state.notifications:
            st.sidebar.header("📢 Notifications")
            for notif in st.session_state.notifications:
                if notif["level"] == "warning":
                    st.sidebar.warning(notif["message"])
                elif notif["level"] == "error":
                    st.sidebar.error(notif["message"])
                else:
                    st.sidebar.info(notif["message"])
            
            if st.sidebar.button("Clear Notifications"):
                st.session_state.notifications = []
