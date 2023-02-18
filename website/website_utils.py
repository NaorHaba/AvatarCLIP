import os
import time
import streamlit as st


import smtplib

from website.config import Config
from website.messages import Messages
from website.settings import settings


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


def request_processed_info(email):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if email is not None:
                st.info(Messages.REQUEST_PROCESSED_INFO_WITH_EMAIL.format(email))
            else:
                st.info(Messages.REQUEST_PROCESSED_INFO)

            func(*args, **kwargs)

        return wrapper

    return decorator


def absolute_path(path):
    return os.path.join(os.path.dirname(__file__), os.pardir, path)


def send_email(recipient_email, subject, body):
    # Send email using Gmail
    smtp_server = 'smtp.gmail.com'
    port = 587

    sender_email = Config.SENDER_EMAIL
    sender_password = os.environ.get('EMAIL_PASSWORD')

    message = f'Subject: {subject}\n\n{body}'
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message)
