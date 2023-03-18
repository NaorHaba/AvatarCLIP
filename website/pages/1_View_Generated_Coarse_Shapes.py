import os
import streamlit as st

from website.config import Config
from website.messages import Messages
from website.settings import Settings
from website.website_utils import render_status, absolute_path

settings = Settings()
st.set_page_config(layout="wide",
                   page_title=Messages.VIEW_GENERATED_COARSE_SHAPES_PAGE_TITLE,
                   page_icon=Config.WEBSITE_ICON_PATH
                   )


coarse_output_folder = absolute_path(os.path.join(settings.settings['OUTPUT_DIR'], settings.settings['COARSE_SHAPE_OUTPUT_DIR']))
if os.path.exists(coarse_output_folder):
    generated_shapes_dirs = os.listdir(coarse_output_folder)
    if len(generated_shapes_dirs) == 0:
        st.write(Messages.NO_SHAPE_FOUND_IN_FOLDER.format(coarse_output_folder))
    else:
        selected_shape = st.selectbox(Messages.VIEW_GENERATED_COARSE_SHAPES_SELECT_SHAPE, generated_shapes_dirs)
        if selected_shape:
            st.markdown(Messages.SELECTED_VIEW_ITEM_TITLE.format(selected_shape))
            shape_dir_path = absolute_path(os.path.join(coarse_output_folder, selected_shape))
            obj_file = absolute_path(os.path.join(shape_dir_path, settings.settings['COARSE_SHAPE_OBJ_OUTPUT_NAME']))
            render_folder = absolute_path(os.path.join(shape_dir_path, settings.settings['COARSE_SHAPE_RENDERING_OUTPUT_DIR']))
            implicit_folder = absolute_path(os.path.join(shape_dir_path, settings.settings['IMPLICIT_AVATAR_OUTPUT_DIR'], "checkpoints"))
            render_status(Messages.VIEW_GENERATED_COARSE_SHAPES_OBJ_FILE_STATUS_TITLE, obj_file)
            render_status(Messages.VIEW_GENERATED_COARSE_SHAPES_RENDER_FOLDER_STATUS_TITLE, render_folder)
            render_status(Messages.VIEW_GENERATED_COARSE_SHAPES_IMPLICIT_FOLDER_STATUS_TITLE, implicit_folder)
else:
    st.info(Messages.FOLDER_DOES_NOT_EXIST.format(coarse_output_folder))
    # TODO ^ change error to indicate that the folder specified in settings.py does not exist