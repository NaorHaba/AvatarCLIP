import os
import streamlit as st
import time

from website.messages import Messages
from website.settings import Settings

st.set_page_config(layout="wide",
                   page_title=Messages.GENERATE_NEW_COARSE_SHAPE_PAGE_TITLE,
                   # page_icon='assets/icon.png'  # TODO
                   )

def generate_coarse_shape(shape_description):
    with st.spinner(text="Generating coarse shape, this may take a while..."):  # TODO move to messages + logging
        for i in range(10):
            time.sleep(1)
        st.success("Done!")  # TODO move to messages + logging


placeholder = st.empty()
with placeholder.form(key="coarse_shape_form", clear_on_submit=False):
    shape_description = st.text_input(Messages.GENERATE_NEW_COARSE_SHAPE_DESCRIPTION, key="shape_description")
    overwrite = st.checkbox(Messages.OVERWRITE_SELECTION, key="overwrite")
    submit = st.form_submit_button(Messages.GENERATE_NEW_COARSE_SHAPE_FORM_SUBMIT_BUTTON)
    shape_folder = os.path.join(Settings.OUTPUT_DIR, Settings.COARSE_SHAPE_OUTPUT_DIR, shape_description)
    obj_file = os.path.join(shape_folder, Settings.COARSE_SHAPE_OBJ_OUTPUT_NAME)
    if submit:
        if os.path.exists(shape_folder) and os.path.exists(obj_file):
            if overwrite:
                st.warning(Messages.OVERWRITE_NOTICE.format(shape_description))
                # TODO call generate_coarse_shape function here
                generate_coarse_shape(shape_description)
            else:
                st.warning(Messages.ALREADY_EXISTS.format(shape_description))
                st.info(Messages.GENERATE_NEW_COARSE_SHAPE_RETRY_MESSAGE.format(shape_description))
        else:
            # TODO call generate_coarse_shape function here
            generate_coarse_shape(shape_description)



    