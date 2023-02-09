import os
import streamlit as st
import time
from website.settings import Settings
from website.utils import render_status

st.set_page_config(layout="wide",
                   page_title="Render Coarse Shape",  # TODO move to config/messages + logging
                   # page_icon='assets/icon.png'  # TODO
                   )

def generate_coarse_shape(shape_description):
    with st.spinner(text="Rendering coarse shape, this may take a while..."):
        for i in range(10):
            time.sleep(1)
        st.success("Done!")

# TODO move hardcoded messages to a config/messages file
coarse_output_folder = os.path.join(Settings.OUTPUT_DIR, Settings.COARSE_SHAPE_OUTPUT_DIR)
if os.path.exists(coarse_output_folder):
    generated_shapes_dirs = os.listdir(coarse_output_folder)
    relevant_shapes_dirs = []
    for shape in generated_shapes_dirs:
        shape_dir_path = os.path.join(coarse_output_folder, shape)
        obj_file = os.path.join(shape_dir_path, Settings.COARSE_SHAPE_OBJ_OUTPUT_NAME)
        if os.path.exists(obj_file):
            relevant_shapes_dirs.append(shape)

    if len(relevant_shapes_dirs) == 0:
        st.info(f"No shapes found in {coarse_output_folder}.")  # TODO move to config/messages + logging
    else:
        placeholder = st.empty()
        with placeholder.form(key="render_coarse_shape_form", clear_on_submit=False):
            selected_shpae = st.selectbox("Select a shape to render", relevant_shapes_dirs)
            overwrite = st.radio(f"If the rendered object exists, do you want to continue or overwrite?", options=('Continue', 'Overwrite', ),key="overwrite", horizontal=True)
            submit = st.form_submit_button("Generate Coarse Shape")
            render_folder = os.path.join(shape_dir_path, Settings.COARSE_SHAPE_RENDERING_OUTPUT_DIR)
            if submit:
                if os.path.exists(render_folder):
                    if overwrite == 'Overwrite':
                        st.warning(f"Overwriting '{selected_shpae}'")
                        # call generate_coarse_shape function here
                        generate_coarse_shape(selected_shpae)
                    else:
                        st.info(f"Continuing '{selected_shpae}' from last checkpoint")
                        generate_coarse_shape(selected_shpae)
                else:
                    # call generate_coarse_shape function here
                    generate_coarse_shape(selected_shpae)

        
else:
    st.info(f"Folder {coarse_output_folder} does not exist.")  # TODO move to config/messages + logging
    # TODO ^ change error to indicate that the folder specified in settings.py does not exist