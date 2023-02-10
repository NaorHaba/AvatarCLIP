import os
from enum import Enum
import time
import streamlit as st


def render_status(text, path):
    if os.path.exists(path):
        icon = ":heavy_check_mark:"
        timestamp_updated = os.path.getmtime(path)

        # Converting the time in seconds to a timestamp
        date_updated = time.ctime(timestamp_updated)
        st.markdown(f"{text}: {icon} (last updated: {date_updated})")
    else:
        icon = ":x:"
        st.markdown(f"{text}: {icon}")

        
class POSE_TYPE(str, Enum):
    STAND_POSE = 'stand_pose'
    T_POSE = 't_pose'
