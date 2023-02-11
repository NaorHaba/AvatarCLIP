import os
import time
import streamlit as st
import sys

import logging

from website.settings import Settings

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('website.log')
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


logger.info('test')


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


# define a decorator that prints st.spinner that runs until the function is done
def spinner(text):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with st.spinner(text):
                func(*args, **kwargs)
            st.success('Done!')

        return wrapper

    return decorator