import os
import streamlit as st

from website.settings import Settings

st.set_page_config(layout="wide",
                   page_title="Generated Coarse Shapes",  # TODO move to config/messages + logging
                   # page_icon='assets/icon.png'  # TODO
                   )


shape_description = st.text_input("Enter a coarse shape description (e.g a tall person, a skinny person etc.):")
shape_folder = os.path.join(Settings.OUTPUT_DIR, Settings.COARSE_SHAPE_OUTPUT_DIR, shape_description)
obj_file = os.path.join(shape_folder, Settings.COARSE_SHAPE_OBJ_OUTPUT_NAME)

if os.path.exists(shape_folder) and os.path.exists(obj_file):
    overwrite = st.checkbox("Object already exists, do you want to overwrite it?")
    if overwrite:
        # call generate_coarse_shape function here
        st.write("Generating coarse shape...")
    else:
        st.write("Going back to last menu.")
else:
    # TODO call generate_coarse_shape function here
    st.write("Generating coarse shape...")
