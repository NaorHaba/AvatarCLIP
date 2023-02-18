import os
import streamlit as st
import time
import yaml
from website.config import Config
from website.website_utils import spinner, send_email_when_done
from website.messages import Messages
from website.settings import settings


st.set_page_config(layout="wide",
                   page_title=Messages.RUN_FROM_FILE_PAGE_TITLE,
                   page_icon=Config.WEBSITE_ICON_PATH
                   )


@send_email_when_done(settings.settings['USER_EMAIL'])
def decorated_run_from_file(data):
    # here we call the function from logic
    pass


st.markdown("#### YAML File Example:")
st.markdown("""```yaml
run_args: [
  {
    coarse_shape_prompt: a tall person,
    texture_description_prompt: a policeman,
    should_continue: false,
    should_overwrite: true,
    convert_to_fbx: true
  },
  {
    coarse_shape_prompt: a short person,
    texture_description_prompt: superman,
    should_continue: false,
    should_overwrite: true,
    convert_to_fbx: true,
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
            decorated_run_from_file(data)
            # # Display the YAML data
            # st.write(data)