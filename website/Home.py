import streamlit as st

from website.config import Config
from website.messages import Messages


st.set_page_config(page_title=Messages.HOME_PAGE_TITLE[2:],
                   page_icon=Config.WEBSITE_ICON_PATH
                   )


st.markdown(Messages.HOME_PAGE_TITLE)
st.markdown(Messages.HOME_PAGE_SUBTITLE)
st.write(Messages.HOME_PAGE_DESCRIPTION)
