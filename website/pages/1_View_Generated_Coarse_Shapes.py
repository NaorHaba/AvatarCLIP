import os
import streamlit as st

from website.settings import Settings
from website.utils import render_status

st.set_page_config(layout="wide",
                   page_title="Generated Coarse Shapes",  # TODO move to config/messages + logging
                   # page_icon='assets/icon.png'  # TODO
                   )


# TODO move hardcoded messages to a config/messages file
coarse_output_folder = os.path.join(Settings.OUTPUT_DIR, Settings.COARSE_SHAPE_OUTPUT_DIR)
if os.path.exists(coarse_output_folder):
    generated_shapes_dirs = os.listdir(coarse_output_folder)
    if len(generated_shapes_dirs) == 0:
        st.write(f"No shapes found in {coarse_output_folder}.")  # TODO move to config/messages + logging
    else:
        selected_shpae = st.selectbox("Select a shape to view", generated_shapes_dirs)
        if selected_shpae:
            st.markdown(f"#### {selected_shpae}")  # TODO move to config/messages + logging
            shape_dir_path = os.path.join(coarse_output_folder, selected_shpae)
            obj_file = os.path.join(shape_dir_path, Settings.COARSE_SHAPE_OBJ_OUTPUT_NAME)
            render_folder = os.path.join(shape_dir_path, Settings.COARSE_SHAPE_RENDERING_OUTPUT_DIR)
            implicit_folder = os.path.join(shape_dir_path, Settings.IMPLICIT_AVATAR_OUTPUT_DIR)
            render_status("OBJ file", obj_file)
            render_status("Render folder", render_folder)
            render_status("Implicit folder", implicit_folder)
        
        # for shape in generated_shapes_dirs:
        #     shape_dir_path = os.path.join(coarse_output_folder, shape)
        #     st.markdown(f"#### {shape}")  # TODO move to config/messages + logging
        #     # check status of shape
        #     obj_file = os.path.join(shape_dir_path, Settings.COARSE_SHAPE_OBJ_OUTPUT_NAME)
        #     render_status("OBJ file", obj_file)  # TODO move to config/messages + logging

        #     render_folder = os.path.join(shape_dir_path, Settings.COARSE_SHAPE_RENDERING_OUTPUT_DIR)
        #     render_status("Render folder", render_folder)  # TODO move to config/messages + logging

        #     implicit_folder = os.path.join(shape_dir_path, Settings.IMPLICIT_AVATAR_OUTPUT_DIR)
        #     render_status("Implicit folder", implicit_folder)  # TODO move to config/messages + logging
else:
    st.write(f"Folder {coarse_output_folder} does not exist.")  # TODO move to config/messages + logging
    # TODO ^ change error to indicate that the folder specified in settings.py does not exist