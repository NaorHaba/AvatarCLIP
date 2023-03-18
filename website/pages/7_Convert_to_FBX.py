import os
import streamlit as st
import time

from website.config import Config
from website.logic_runner import run_convert_to_fbx
from website.messages import Messages
from website.settings import Settings
from website.website_utils import absolute_path

settings = Settings()
st.set_page_config(layout="wide",
                   page_title=Messages.CONVERT_TO_FBX_PAGE_TITLE,
                   page_icon=Config.WEBSITE_ICON_PATH
                   )


avatar_output_folder = absolute_path(os.path.join(settings.settings['OUTPUT_DIR'], settings.settings['GENERATED_AVATAR_OUTPUT_DIR']))
if os.path.exists(avatar_output_folder):
    generated_avatars_dirs = os.listdir(avatar_output_folder)
    relevant_avatars_dirs = []
    for avatar in generated_avatars_dirs:
        avatar_dir_path = os.path.join(avatar_output_folder, avatar)
        texture_folder = os.path.join(avatar_dir_path, settings.settings['GENERATED_AVATAR_TEXTURE_OUTPUT_DIR'])
        if os.path.exists(texture_folder):
            relevant_avatars_dirs.append(avatar)

    if len(relevant_avatars_dirs) == 0:
        st.info(Messages.NO_SHAPE_FOUND_IN_FOLDER.format(avatar_output_folder))
    else:
        placeholder = st.empty()
        with placeholder.form(key="render_coarse_shape_form", clear_on_submit=False):
            selected_avatar = st.selectbox(Messages.CONVERT_TO_FBX_SELECT_AVATAR, relevant_avatars_dirs, key="selected_avatar")
            selected_avatar_dir_path = os.path.join(avatar_output_folder, selected_avatar)
            overwrite = st.checkbox(Messages.OVERWRITE_SELECTION, key="overwrite")
            submit = st.form_submit_button(Messages.CONVERT_TO_FBX_FORM_SUBMIT_BUTTON)
            fbx_file = os.path.join(selected_avatar_dir_path, settings.settings['GENERATED_AVATAR_FBX_OUTPUT_NAME'])
            if submit:
                avatar_dir_path = os.path.join(avatar_output_folder, selected_avatar)
                texture_folder = os.path.join(avatar_dir_path, settings.settings['GENERATED_AVATAR_TEXTURE_OUTPUT_DIR'])

                meshes_folder = os.path.join(texture_folder, "meshes")
                mesh_file = os.path.join(meshes_folder, sorted(os.listdir(meshes_folder))[-1])
                if os.path.exists(fbx_file):
                    if overwrite:
                        st.warning(Messages.OVERWRITE_NOTICE.format(fbx_file))
                        st.info(Messages.CONVERT_TO_FBX_MESH_FILE.format(mesh_file))
                        # call generate_coarse_shape function here
                        run_convert_to_fbx(mesh_file, fbx_file)
                    else:
                        st.warning(Messages.ALREADY_EXISTS.format(fbx_file))
                        st.info(Messages.CONVERT_TO_FBX_RETRY_MESSAGE.format(selected_avatar))

                else:
                    # call generate_coarse_shape function here
                    st.info(Messages.CONVERT_TO_FBX_MESH_FILE.format(mesh_file))
                    run_convert_to_fbx(mesh_file, fbx_file)
else:
    st.info(Messages.FOLDER_DOES_NOT_EXIST.format(avatar_output_folder))