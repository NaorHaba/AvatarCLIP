import os
import streamlit as st
import yaml
from website.logic_runner import run_all
from website.config import Config
from website.messages import Messages
from website.settings import settings


st.set_page_config(layout="wide",
                   page_title=Messages.RUN_FROM_FILE_PAGE_TITLE,
                   page_icon=Config.WEBSITE_ICON_PATH
                   )

st.markdown("#### YAML File Example:")
st.markdown("""```yaml
run_args: [
  {
    coarse_shape_prompt: a tall person,
    texture_description_prompt: a policeman,
    should_continue: false,
    should_overwrite: true,
    config_type: large
  },
  {
    coarse_shape_prompt: a short person,
    texture_description_prompt: superman,
    should_continue: false,
    should_overwrite: true,
    config_type: small,
  },
  ...
  ]
""")

placeholder = st.empty()
with placeholder.form(key="render_coarse_shape_form", clear_on_submit=False):
    uploaded_file = st.file_uploader("Choose a YAML file to upload and run", type="yaml")
    submit = st.form_submit_button(Messages.RUN_FROM_FILE_FORM_SUBMIT_BUTTON)
    if submit:
        if uploaded_file is not None:
            # Read the file contents
            file_contents = uploaded_file.read()

            # Parse the YAML file
            data = yaml.safe_load(file_contents)

            # send the YAML file to the BE to run
            run_all(data)
            # # Display the YAML data
            # st.write(data)