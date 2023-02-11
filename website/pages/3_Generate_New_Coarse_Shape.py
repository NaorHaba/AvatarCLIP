import os
import streamlit as st
import time
from website.website_utils import spinner
from website.logic import generate_coarse_shape

from website.messages import Messages
from website.settings import Settings


st.set_page_config(layout="wide",
                   page_title=Messages.GENERATE_NEW_COARSE_SHAPE_PAGE_TITLE,
                   # page_icon='assets/icon.png'  # TODO
                   )

@spinner("Generating coarse shape, this may take a while...")
def decorated_generate_coarse_shape(shape_description):
    generate_coarse_shape(shape_description)


placeholder = st.empty()
with placeholder.form(key="coarse_shape_form", clear_on_submit=False):
    shape_description = st.text_input(Messages.GENERATE_NEW_COARSE_SHAPE_DESCRIPTION, key="shape_description")
    overwrite = st.checkbox(Messages.OVERWRITE_SELECTION, key="overwrite")
    submit = st.form_submit_button(Messages.GENERATE_NEW_COARSE_SHAPE_FORM_SUBMIT_BUTTON)
    shape_folder = Settings.absolute_path(os.path.join(Settings.OUTPUT_DIR, Settings.COARSE_SHAPE_OUTPUT_DIR, shape_description))
    obj_file = Settings.absolute_path(os.path.join(shape_folder, Settings.COARSE_SHAPE_OBJ_OUTPUT_NAME))
    if submit:
        if os.path.exists(shape_folder) and os.path.exists(obj_file):
            if overwrite:
                st.warning(Messages.OVERWRITE_NOTICE.format(shape_description))
                decorated_generate_coarse_shape(shape_description)
            else:
                st.warning(Messages.ALREADY_EXISTS.format(shape_description))
                st.info(Messages.GENERATE_NEW_COARSE_SHAPE_RETRY_MESSAGE.format(shape_description))
        else:
            decorated_generate_coarse_shape(shape_description)
