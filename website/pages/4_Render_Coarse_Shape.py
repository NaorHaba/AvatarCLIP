import os
import streamlit as st

from website.config import Config
from website.logic_runner import run_render_coarse_shape
from website.website_utils import absolute_path
from website.messages import Messages
from website.settings import Settings

settings = Settings()
st.set_page_config(layout="wide",
                   page_title=Messages.RENDER_COARSE_SHAPE_PAGE_TITLE,
                   page_icon=Config.WEBSITE_ICON_PATH
                   )


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
            overwrite = st.checkbox(Messages.OVERWRITE_SELECTION, key="overwrite")
            submit = st.form_submit_button(Messages.RENDER_COARSE_SHAPE_FORM_SUBMIT_BUTTON)
            render_folder = os.path.join(coarse_output_folder, selected_shape, settings.settings['COARSE_SHAPE_RENDERING_OUTPUT_DIR'])
            obj_file = os.path.join(selected_shape, settings.settings['COARSE_SHAPE_OBJ_OUTPUT_NAME'])
            path_to_obj = os.path.join(coarse_output_folder, obj_file)
            if submit:
                if os.path.exists(render_folder):
                    if overwrite:
                        st.warning(Messages.OVERWRITE_NOTICE.format(render_folder))
                        # call generate_coarse_shape function here
                        run_render_coarse_shape(path_to_obj)
                    else:
                        st.warning(Messages.ALREADY_EXISTS.format(selected_shape))
                        st.info(Messages.RENDER_COARSE_SHAPE_RETRY_MESSAGE.format(selected_shape))
                else:
                    # call generate_coarse_shape function here
                    run_render_coarse_shape(path_to_obj)
else:
    st.info(Messages.FOLDER_DOES_NOT_EXIST.format(coarse_output_folder))