import os
import streamlit as st
import time

from website.config import Config
from website.logic_runner import run_generate_textures
from website.messages import Messages
from website.settings import Settings
from website.website_utils import absolute_path


settings = Settings()
st.set_page_config(layout="wide",
                   page_title=Messages.GENERATE_TEXTURES_PAGE_TITLE,
                   page_icon=Config.WEBSITE_ICON_PATH
                   )


coarse_output_folder = absolute_path(os.path.join(settings.settings['OUTPUT_DIR'], settings.settings['COARSE_SHAPE_OUTPUT_DIR']))
if os.path.exists(coarse_output_folder):
    generated_shapes_dirs = os.listdir(coarse_output_folder)
    relevant_shapes_dirs = []
    for shape in generated_shapes_dirs:
        shape_dir_path = os.path.join(coarse_output_folder, shape)
        implicit_folder = os.path.join(shape_dir_path, settings.settings['IMPLICIT_AVATAR_OUTPUT_DIR'], "checkpoints")
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
            submit = st.form_submit_button(Messages.GENERATE_TEXTURES_FORM_SUBMIT_BUTTON)
            avatar_output_folder = absolute_path(os.path.join(settings.settings['OUTPUT_DIR'], settings.settings['GENERATED_AVATAR_OUTPUT_DIR']))
            if submit:                
                if choose_config == Messages.LARGE_CONFIG:
                    implicit_config = settings.settings['LARGE_AVATAR_TEXTURE_CONFIG']
                else:
                    implicit_config = settings.settings['SMALL_AVATAR_TEXTURE_CONFIG']
                
                selected_shape_dir = os.path.join(coarse_output_folder, selected_shape)
                selected_avatar = f"{texture_description} ({selected_shape})"
                avatar_dir_path = os.path.join(avatar_output_folder, selected_avatar)
                texture_folder = os.path.join(avatar_dir_path, settings.settings['GENERATED_AVATAR_TEXTURE_OUTPUT_DIR'], "checkpoints")
                if os.path.exists(texture_folder):
                    if if_exists_instruction == Messages.OVERWRITE_SELECTION:
                        st.warning(Messages.OVERWRITE_NOTICE.format(texture_folder))
                        run_generate_textures(texture_description, implicit_config, selected_shape_dir, selected_avatar, False)
                    else:
                        st.info(Messages.CONTINUE_NOTICE.format(texture_folder))
                        run_generate_textures(texture_description, implicit_config, selected_shape_dir, selected_avatar, True)
                else:
                    run_generate_textures(texture_description, implicit_config, selected_shape_dir, selected_avatar, False)
else:
    st.info(Messages.FOLDER_DOES_NOT_EXIST.format(coarse_output_folder))