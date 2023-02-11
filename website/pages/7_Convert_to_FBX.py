import os
import streamlit as st
import time
from website.website_utils import spinner
from website.logic import convert_to_FBX
from website.messages import Messages
from website.settings import Settings

st.set_page_config(layout="wide",
                   page_title=Messages.CONVERT_TO_FBX_PAGE_TITLE,
                   # page_icon='assets/icon.png'  # TODO
                   )

@spinner(text="Converting to FBX, this may take a while...")
def decorated_convert_to_FBX():
    convert_to_FBX()


def generate_coarse_shape(shape_description):
    with st.spinner(text="Converting to FBX, this may take a while..."):  # TODO move to config/messages + logging
        for i in range(10):
            time.sleep(1)
        st.success("Done!")  # TODO move to config/messages + logging


avatar_output_folder = os.path.join(Settings.OUTPUT_DIR, Settings.GENERATED_AVATAR_OUTPUT_DIR)
if os.path.exists(avatar_output_folder):
    generated_avatars_dirs = os.listdir(avatar_output_folder)
    relevant_avatars_dirs = []
    for avatar in generated_avatars_dirs:
        avatar_dir_path = os.path.join(avatar_output_folder, avatar)
        texture_folder = os.path.join(avatar_dir_path, Settings.GENERATED_AVATAR_TEXTURE_OUTPUT_DIR)
        if os.path.exists(texture_folder):
            relevant_avatars_dirs.append(avatar)

    if len(relevant_avatars_dirs) == 0:
        st.info(Messages.NO_SHAPE_FOUND_IN_FOLDER.format(avatar_output_folder))
    else:
        placeholder = st.empty()
        with placeholder.form(key="render_coarse_shape_form", clear_on_submit=False):
            selected_avatar = st.selectbox(Messages.CONVERT_TO_FBX_SELECT_AVATAR, relevant_avatars_dirs, key="selected_avatar")
            overwrite = st.checkbox(Messages.OVERWRITE_SELECTION, key="overwrite")
            submit = st.form_submit_button(Messages.CONVERT_TO_FBX_FORM_SUBMIT_BUTTON)
            fbx_file = os.path.join(avatar_dir_path, Settings.GENERATED_AVATAR_FBX_OUTPUT_NAME)
            if submit:
                avatar_dir_path = os.path.join(avatar_output_folder, avatar)
                texture_folder = os.path.join(avatar_dir_path, Settings.GENERATED_AVATAR_TEXTURE_OUTPUT_DIR)
                if os.path.exists(fbx_file):
                    if overwrite == Messages.OVERWRITE_SELECTION:
                        st.warning(Messages.OVERWRITE_NOTICE.format(fbx_file))
                        # call generate_coarse_shape function here
                        decorated_convert_to_FBX(texture_folder)
                    else:
                        st.warning(Messages.ALREADY_EXISTS.format(fbx_file))
                        st.info(Messages.CONVERT_TO_FBX_RETRY_MESSAGE.format(selected_avatar))

                else:
                    # call generate_coarse_shape function here
                    decorated_convert_to_FBX(texture_folder)
else:
    st.info(Messages.FOLDER_DOES_NOT_EXIST.format(avatar_output_folder))
    # TODO ^ change error to indicate that the folder specified in settings.py does not exist