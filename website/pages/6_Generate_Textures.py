import os
import streamlit as st
import time

from website.messages import Messages
from website.settings import Settings

st.set_page_config(layout="wide",
                   page_title=Messages.GENERATE_TEXTURES_PAGE_TITLE,
                   # page_icon='assets/icon.png'  # TODO
                   )

def generate_coarse_shape(shape_description, choose_config):
    with st.spinner(text="Rendering textures, this may take a while..."):  # TODO move to config/messages + logging
        for i in range(10):
            time.sleep(1)
        st.success("Done!")  # TODO move to config/messages + logging


coarse_output_folder = os.path.join(Settings.OUTPUT_DIR, Settings.COARSE_SHAPE_OUTPUT_DIR)
if os.path.exists(coarse_output_folder):
    generated_shapes_dirs = os.listdir(coarse_output_folder)
    relevant_shapes_dirs = []
    for shape in generated_shapes_dirs:
        shape_dir_path = os.path.join(coarse_output_folder, shape)
        implicit_folder = os.path.join(shape_dir_path, Settings.IMPLICIT_AVATAR_OUTPUT_DIR)
        if os.path.exists(implicit_folder):
            relevant_shapes_dirs.append(shape)

    if len(relevant_shapes_dirs) == 0:
        st.info(Messages.NO_SHAPE_FOUND_IN_FOLDER.format(coarse_output_folder))
    else:
        placeholder = st.empty()
        with placeholder.form(key="generate_textures_form", clear_on_submit=False):
            selected_shape = st.selectbox(Messages.GENERATE_TEXTURES_SELECT_SHAPE, relevant_shapes_dirs, key="selected_shape")
            texture_description = st.text_input(Messages.GENERATE_TEXTURES_DESCRIPTION, key="texture_description")
            if_exists_instruction = st.radio(Messages.IF_EXISTS_INSTRUCTION, options=(Messages.CONTINUE_SELECTION, Messages.OVERWRITE_SELECTION), key="if_exists_instruction")
            choose_config = st.radio(Messages.CHOOSE_CONFIG, options=(Messages.LARGE_CONFIG, Messages.SMALL_CONFIG), key="choose_config")
            submit = st.form_submit_button(Messages.INITIALIZE_IMPLICIT_AVATAR_FORM_SUBMIT_BUTTON)
            avatar_output_folder = os.path.join(Settings.OUTPUT_DIR, Settings.GENERATED_AVATAR_OUTPUT_DIR)
            if submit:
                selected_avatar = f"{texture_description} ({selected_shape})"
                avatar_dir_path = os.path.join(avatar_output_folder, selected_avatar)
                texture_folder = os.path.join(avatar_dir_path, Settings.GENERATED_AVATAR_TEXTURE_OUTPUT_DIR)
                if os.path.exists(texture_folder):
                    if if_exists_instruction == Messages.OVERWRITE_SELECTION:
                        st.warning(Messages.OVERWRITE_NOTICE.format(texture_folder))
                        # call init_imp_avatar function here
                        generate_coarse_shape(selected_shape, choose_config)
                    else:
                        st.info(Messages.CONTINUE_NOTICE.format(selected_shape))
                        generate_coarse_shape(selected_shape, choose_config)
                else:
                    # call init_imp_avatar function here
                    generate_coarse_shape(selected_shape, choose_config)
else:
    st.info(Messages.FOLDER_DOES_NOT_EXIST.format(coarse_output_folder))
    # TODO ^ change error to indicate that the folder specified in settings.py does not exist