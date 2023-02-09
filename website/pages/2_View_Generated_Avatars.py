import os
import streamlit as st

from website.settings import Settings
from website.utils import render_status

st.set_page_config(layout="wide",
                   page_title="Generated Avatars",  # TODO move to config/messages + logging
                   # page_icon='assets/icon.png'  # TODO
                   )


# TODO move hardcoded messages to a config/messages file
avatar_output_folder = os.path.join(Settings.OUTPUT_DIR, Settings.GENERATED_AVATAR_OUTPUT_DIR)
if os.path.exists(avatar_output_folder):
    generated_avatars_dirs = os.listdir(avatar_output_folder)
    if len(generated_avatars_dirs) == 0:
        st.write(f"No shapes found in {generated_avatars_dirs}.")  # TODO move to config/messages + logging
    else:
        for avatar in generated_avatars_dirs:
            avatar_dir_path = os.path.join(avatar_output_folder, avatar)
            st.markdown(f"#### {avatar}")  # TODO move to config/messages + logging

            # check status of shape
            # TODO add checks for running folder and fbx file
            # render_folder = os.path.join(avatar_dir_path, Settings.GENERATED_AVATAR_OUTPUT_DIR)
            # render_status("Render folder", render_folder)  # TODO move to config/messages + logging
            #
            # obj_file = os.path.join(avatar_dir_path, avatar + ".fbx")
            # render_status("OBJ file", obj_file)  # TODO move to config/messages + logging
else:
    st.write(f"Folder {avatar_output_folder} does not exist.")  # TODO move to config/messages + logging
    # TODO ^ change error to indicate that the folder specified in settings.py does not exist
