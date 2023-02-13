import os
import streamlit as st
import time

from website.config import Config
from website.website_utils import spinner, absolute_path
from website.logic import render_coarse_shape_wrapper
from website.messages import Messages
from website.settings import settings


st.set_page_config(layout="wide",
                   page_title=Messages.RENDER_COARSE_SHAPE_PAGE_TITLE,
                   page_icon=Config.WEBSITE_ICON_PATH
                   )


@spinner(Messages.RENDER_COARSE_SHAPE_SPINNER_MESSAGE)
def decorated_render_coarse_shape(path_to_obj_file):
    render_coarse_shape_wrapper(path_to_obj_file)


coarse_output_folder = absolute_path(os.path.join(settings.settings['OUTPUT_DIR'], settings.settings['COARSE_SHAPE_OUTPUT_DIR']))
if os.path.exists(coarse_output_folder):
    generated_shapes_dirs = os.listdir(coarse_output_folder)
    relevant_shapes_dirs = []
    for shape in generated_shapes_dirs:
        shape_dir_path = absolute_path(os.path.join(coarse_output_folder, shape))
        obj_file = absolute_path(os.path.join(shape_dir_path, settings.settings['COARSE_SHAPE_OBJ_OUTPUT_NAME']))
        if os.path.exists(obj_file):
            relevant_shapes_dirs.append(shape)

    if len(relevant_shapes_dirs) == 0:
        st.info(Messages.NO_SHAPE_FOUND_IN_FOLDER.format(coarse_output_folder))
    else:
        placeholder = st.empty()
        with placeholder.form(key="render_coarse_shape_form", clear_on_submit=False):
            selected_shape = st.selectbox(Messages.RENDER_COARSE_SHAPE_SELECT_SHAPE, relevant_shapes_dirs, key="selected_shape")
            if_exists_instruction = st.radio(Messages.IF_EXISTS_INSTRUCTION, options=(Messages.CONTINUE_SELECTION, Messages.OVERWRITE_SELECTION), key="if_exists_instruction")
            submit = st.form_submit_button(Messages.RENDER_COARSE_SHAPE_FORM_SUBMIT_BUTTON)
            render_folder = absolute_path(os.path.join(selected_shape, settings.settings['COARSE_SHAPE_RENDERING_OUTPUT_DIR']))
            obj_file = absolute_path(os.path.join(selected_shape, settings.settings['COARSE_SHAPE_OBJ_OUTPUT_NAME']))
            path_to_obj = absolute_path(os.path.join(coarse_output_folder, obj_file))
            if submit:
                if os.path.exists(render_folder):
                    if if_exists_instruction == Messages.OVERWRITE_SELECTION:
                        st.warning(Messages.OVERWRITE_NOTICE.format(render_folder))
                        # call generate_coarse_shape function here
                        decorated_render_coarse_shape(path_to_obj)
                    else:
                        st.info(Messages.CONTINUE_NOTICE.format(selected_shape))
                        decorated_render_coarse_shape(path_to_obj)
                else:
                    # call generate_coarse_shape function here
                    decorated_render_coarse_shape(path_to_obj)
else:
    st.info(Messages.FOLDER_DOES_NOT_EXIST.format(coarse_output_folder))
    # TODO ^ change error to indicate that the folder specified in settings.py does not exist