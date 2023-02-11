import os
import streamlit as st
import time
from website.website_utils import spinner
from website.logic import initialize_implicit_avatar
from website.messages import Messages
from website.settings import Settings

st.set_page_config(layout="wide",
                   page_title=Messages.INITIALIZE_IMPLICIT_AVATAR_PAGE_TITLE,
                   # page_icon='assets/icon.png'  # TODO
                   )


@spinner("Initializing implicit avatar, this may take a while...")
def decorated_init_implicit_avatar(implicit_config, path_to_render, is_continue):
    initialize_implicit_avatar(implicit_config, path_to_render, is_continue)


coarse_output_folder = Settings.absolute_path(os.path.join(Settings.OUTPUT_DIR, Settings.COARSE_SHAPE_OUTPUT_DIR))
if os.path.exists(coarse_output_folder):
    generated_shapes_dirs = Settings.absolute_path(os.listdir(coarse_output_folder))
    relevant_shapes_dirs = []
    for shape in generated_shapes_dirs:
        shape_dir_path = Settings.absolute_path(os.path.join(coarse_output_folder, shape))
        render_folder = Settings.absolute_path(os.path.join(shape_dir_path, Settings.COARSE_SHAPE_RENDERING_OUTPUT_DIR))
        if os.path.exists(render_folder):
            relevant_shapes_dirs.append(shape)

    if len(relevant_shapes_dirs) == 0:
        st.info(Messages.NO_SHAPE_FOUND_IN_FOLDER.format(coarse_output_folder))
    else:
        placeholder = st.empty()
        with placeholder.form(key="init_implicit_avatar_form", clear_on_submit=False):
            selected_shape = st.selectbox(Messages.INITIALIZE_IMPLICIT_AVATAR_SELECT_SHAPE, relevant_shapes_dirs, key="selected_shape")
            if_exists_instruction = st.radio(Messages.IF_EXISTS_INSTRUCTION, options=(Messages.CONTINUE_SELECTION, Messages.OVERWRITE_SELECTION), key="if_exists_instruction")
            choose_config = st.radio(Messages.CHOOSE_CONFIG, options=(Messages.LARGE_CONFIG, Messages.SMALL_CONFIG), key="choose_config")
            submit = st.form_submit_button(Messages.INITIALIZE_IMPLICIT_AVATAR_FORM_SUBMIT_BUTTON)
            implicit_folder = Settings.absolute_path(os.path.join(selected_shape, Settings.IMPLICIT_AVATAR_OUTPUT_DIR))
            if submit:
                if choose_config == Messages.LARGE_CONFIG:
                    implicit_config = Settings.LARGE_IMPLICIT_AVATAR_CONFIG
                else:
                    implicit_config = Settings.SMALL_IMPLICIT_AVATAR_CONFIG

                shape_folder = Settings.absolute_path(os.path.join(coarse_output_folder, selected_shape))
                if os.path.exists(implicit_folder):
                    if if_exists_instruction == Messages.OVERWRITE_SELECTION:
                        print(1)
                        st.warning(Messages.OVERWRITE_NOTICE.format(implicit_folder))
                        decorated_init_implicit_avatar(implicit_config, shape_folder, False)
                    else:
                        print(2)
                        st.info(Messages.CONTINUE_NOTICE.format(selected_shape))
                        decorated_init_implicit_avatar(implicit_config, shape_folder, True)
                else:
                    print(3)
                    decorated_init_implicit_avatar(implicit_config, shape_folder, False)
else:
    st.info(Messages.FOLDER_DOES_NOT_EXIST.format(coarse_output_folder))
    # TODO ^ change error to indicate that the folder specified in settings.py does not exist