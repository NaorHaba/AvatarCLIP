import os
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


def spinner(text):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with st.spinner(text):
                func(*args, **kwargs)
            st.success('Done!')

        return wrapper

    return decorator


def send_email_when_done(email):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if email is not None:
                st.info(f"Your request is being processed. You will receive an email to {email} when it's done.")
            else:
                st.info("Your request is being processed. You can check the status in the logs.")

            func(*args, **kwargs)
            # TODO send email

        return wrapper

    return decorator


def absolute_path(path):
    return os.path.join(os.path.dirname(__file__), os.pardir, path)