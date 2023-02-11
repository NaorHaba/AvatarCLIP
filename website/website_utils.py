import os
import time
import streamlit as st
import sys

import logging

from website.settings import Settings


def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s()]: %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    file_handler = logging.FileHandler(Settings.absolute_path(Settings.LOGS_DIR + Settings.LOG_FILE_NAME))
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


stdout_logger = get_logger('STDOUT')
sl = StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl

stderr_logger = get_logger('STDERR')
sl = StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl


print('hello world')


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