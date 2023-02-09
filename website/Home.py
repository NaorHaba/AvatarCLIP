import os
import sys
import streamlit as st

st.set_page_config(layout="wide",
                   page_title="Generated Coarse Shapes",  # TODO move to config/messages + logging
                   # page_icon='assets/icon.png'  # TODO
                   )


st.markdown("# AVR Project - AvatarCLIP")
st.markdown('## An interactive tool for generating 3D avatars using AvatarCLIP')
st.write("This project is a web application that allows users to generate 3D avatars using AvatarCLIP.")  # TODO