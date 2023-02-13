import os
import streamlit as st

from website.config import Config
from website.messages import Messages
from website.settings import settings
from website.website_utils import render_status, absolute_path

st.set_page_config(layout="wide",
                   page_title=Messages.VIEW_GENERATED_COARSE_SHAPES_PAGE_TITLE,
                   page_icon=Config.WEBSITE_ICON_PATH
                   )


avatar_output_folder = absolute_path(os.path.join(settings.settings['OUTPUT_DIR'], settings.settings['GENERATED_AVATAR_OUTPUT_DIR']))
if os.path.exists(avatar_output_folder):
    generated_avatars_dirs = os.listdir(avatar_output_folder)
    if len(generated_avatars_dirs) == 0:
        st.write(Messages.NO_SHAPE_FOUND_IN_FOLDER.format(avatar_output_folder))
    else:
        selected_avatar = st.selectbox(Messages.VIEW_GENERATED_AVATARS_SELECT_AVATAR, generated_avatars_dirs)
        if selected_avatar:
            st.markdown(Messages.SELECTED_VIEW_ITEM_TITLE.format(selected_avatar))
            avatar_dir_path = absolute_path(os.path.join(avatar_output_folder, selected_avatar))
            texture_folder = absolute_path(os.path.join(avatar_dir_path, settings.settings['GENERATED_AVATAR_TEXTURE_OUTPUT_DIR']))
            fbx_file = absolute_path(os.path.join(avatar_dir_path, settings.settings['GENERATED_AVATAR_FBX_OUTPUT_NAME']))
            render_status(Messages.VIEW_GENERATED_AVATARS_TEXTURE_FOLDER_STATUS_TITLE, texture_folder)
            render_status(Messages.VIEW_GENERATED_AVATARS_FBX_FILE_STATUS_TITLE, fbx_file)
else:
    st.info(Messages.FOLDER_DOES_NOT_EXIST.format(avatar_output_folder))
    # TODO ^ change error to indicate that the folder specified in settings.py does not exist
