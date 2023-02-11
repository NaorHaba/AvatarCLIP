import os
import time
import streamlit as st
import sys

import logging

from website.settings import Settings


class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())


# Create logger
logger = logging.getLogger()
if Settings.LOG_TO_FILE:
    # initialize logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s()]: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=f'{Settings.LOGS_DIR}{time.strftime("%Y%m%d-%H%M%S")}.log',
                        filemode='w')
else:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s()]: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

# Redirect stdout to logger
sys.stdout = StreamToLogger(logger, logging.INFO)
sys.stderr = StreamToLogger(logger, logging.ERROR)


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

