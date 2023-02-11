import yaml
import streamlit as st

# Load the saved settings
def load_settings():
    with open("website/settings.yaml", "r") as f:
        return yaml.safe_load(f)

# Save the settings
def save_settings(settings):
    with open("website/settings.yaml", "w") as f:
        yaml.dump(settings, f)

st.set_page_config(layout="wide",
                   page_title="Settings",
                   # page_icon='assets/icon.png'  # TODO
                   )

settings = load_settings()
placeholder = st.empty()
with placeholder.form(key="settings_form", clear_on_submit=False):
    for key, val in sorted(settings.items()):
        if type(val) == bool:
            settings[key] = st.checkbox(key, value=val)
        else:
            settings[key] = st.text_input(key, value=val)
    
    submit = st.form_submit_button("Save")
    if submit:
        save_settings(settings)
        st.success("Settings saved!")
    