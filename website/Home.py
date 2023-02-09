import os
import sys
import streamlit as st

from website.messages import Messages

st.markdown(Messages.HOME_PAGE_TITLE)
st.markdown(Messages.HOME_PAGE_SUBTITLE)
st.write(Messages.HOME_PAGE_DESCRIPTION)