import os
import streamlit as st

from website.config import Config
from website.logic_runner import run_generate_coarse_shape
from website.website_utils import absolute_path

from website.messages import Messages
from website.settings import Settings

settings = Settings()
st.set_page_config(layout="wide",
                   page_title=Messages.GENERATE_NEW_COARSE_SHAPE_PAGE_TITLE,
                   page_icon=Config.WEBSITE_ICON_PATH
                   )


placeholder = st.empty()
with placeholder.form(key="coarse_shape_form", clear_on_submit=False):
    shape_description = st.text_input(Messages.GENERATE_NEW_COARSE_SHAPE_DESCRIPTION, key="shape_description")
    overwrite = st.checkbox(Messages.OVERWRITE_SELECTION, key="overwrite")
    submit = st.form_submit_button(Messages.GENERATE_NEW_COARSE_SHAPE_FORM_SUBMIT_BUTTON)
    shape_folder = absolute_path(os.path.join(settings.settings['OUTPUT_DIR'], settings.settings['COARSE_SHAPE_OUTPUT_DIR'], shape_description))
    obj_file = absolute_path(os.path.join(shape_folder, settings.settings['COARSE_SHAPE_OBJ_OUTPUT_NAME']))
    if submit:
        if os.path.exists(shape_folder) and os.path.exists(obj_file):
            if overwrite:
                st.warning(Messages.OVERWRITE_NOTICE.format(shape_description))
                run_generate_coarse_shape(shape_description)
            else:
                st.warning(Messages.ALREADY_EXISTS.format(shape_description))
                st.info(Messages.GENERATE_NEW_COARSE_SHAPE_RETRY_MESSAGE.format(shape_description))
        else:
            run_generate_coarse_shape(shape_description)
