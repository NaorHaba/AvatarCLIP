import os
import streamlit as st
import time
from website.settings import Settings

st.set_page_config(layout="wide",
                   page_title="Generated Coarse Shapes",  # TODO move to config/messages + logging
                   # page_icon='assets/icon.png'  # TODO
                   )

def generate_coarse_shape(shape_description):
    with st.spinner(text="Generating coarse shape, this may take a while..."):
        for i in range(10):
            time.sleep(1)
        st.success("Done!")


placeholder = st.empty()
with placeholder.form(key="coarse_shape_form", clear_on_submit=False):
    shape_description = st.text_input("Enter a coarse shape description (e.g a tall person, a skinny person etc.):", key="shape_description")
    overwrite = st.checkbox(f"Do you want to overwrite if exists?", key="overwrite")
    submit = st.form_submit_button("Generate Coarse Shape")
    shape_folder = os.path.join(Settings.OUTPUT_DIR, Settings.COARSE_SHAPE_OUTPUT_DIR, shape_description)
    obj_file = os.path.join(shape_folder, Settings.COARSE_SHAPE_OBJ_OUTPUT_NAME)
    if submit:
        if os.path.exists(shape_folder) and os.path.exists(obj_file):
            if overwrite:
                st.warning(f"Overwriting '{shape_description}'")
                # call generate_coarse_shape function here
                generate_coarse_shape(shape_description)
            else:
                st.warning(f"'{shape_description}' already exists")
                st.info(f"Please choose a different description or check the overwrite checkbox")
        else:
            # call generate_coarse_shape function here
            generate_coarse_shape(shape_description)



    