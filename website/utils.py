import os
from enum import Enum

import streamlit as st


def render_status(text, path):
    icon = ":heavy_check_mark:" if os.path.exists(path) else ":x:"
    st.markdown(f"{text}: {icon}")


class POSE_TYPE(str, Enum):
    STAND_POSE = 'stand_pose'
    T_POSE = 't_pose'
