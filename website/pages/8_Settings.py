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
new_settings = dict()
with placeholder.form(key="settings_form", clear_on_submit=False):
    st.markdown("## Email:")
    new_settings["EMAIL"] = st.text_input("Email", value=settings["EMAIL"])

    st.markdown("## Model Directories:")
    new_settings["SMPL_MODEL_DIR"] = st.text_input("SMPL Model Directory", value=settings["SMPL_MODEL_DIR"])
    new_settings["VIRTUAL_AUTO_ENCODER_PATH"] = st.text_input("Virtual Auto Encoder Path", value=settings["VIRTUAL_AUTO_ENCODER_PATH"])
    new_settings["CODEBOOK_PATH"] = st.text_input("Codebook Path", value=settings["CODEBOOK_PATH"])
    new_settings["STAND_POSE_PATH"] = st.text_input("Stand Pose Path", value=settings["STAND_POSE_PATH"])

    st.markdown("## Prompt Settings:")
    new_settings["ENHANCE_PROMPT"] = st.checkbox("Enhance Prompt", value=settings["ENHANCE_PROMPT"])
    new_settings["PROMPT_ENHANCING"] = st.text_input("Prompt Enhancing", value=settings["PROMPT_ENHANCING"])
    new_settings["FACE_PROMPT_WRAP"] = st.text_input("Face Prompt Wrap", value=settings["FACE_PROMPT_WRAP"])
    new_settings["BACK_PROMPT_WRAP"] = st.text_input("Back Prompt Wrap", value=settings["BACK_PROMPT_WRAP"])
    new_settings["NEUTRAL_BODY_SHAPE_PROMPT"] = st.text_input("Neutral Body Shape Prompt", value=settings["NEUTRAL_BODY_SHAPE_PROMPT"])
    
    st.markdown("## Pose Settings:")
    pose_type = st.radio("Pose Type", options=["Stand Pose", "T-Pose"], index=0 if settings["POSE_TYPE"] == "stand_pose" else 1)
    
    st.markdown("## Implicit Avatar Configurations:")
    new_settings["SMALL_IMPLICIT_AVATAR_CONFIG"] = st.text_input("Small Implicit Avatar Config", value=settings["SMALL_IMPLICIT_AVATAR_CONFIG"])
    new_settings["LARGE_IMPLICIT_AVATAR_CONFIG"] = st.text_input("Large Implicit Avatar Config", value=settings["LARGE_IMPLICIT_AVATAR_CONFIG"])
    
    st.markdown("## Avatar Texture Configurations:")
    new_settings["SMALL_AVATAR_TEXTURE_CONFIG"] = st.text_input("Small Avatar Texture Config", value=settings["SMALL_AVATAR_TEXTURE_CONFIG"])
    new_settings["LARGE_AVATAR_TEXTURE_CONFIG"] = st.text_input("Large Avatar Texture Config", value=settings["LARGE_AVATAR_TEXTURE_CONFIG"])
    
    st.markdown("## Output Directories:")
    new_settings["OUTPUT_DIR"] = st.text_input("Output Directory", value=settings["OUTPUT_DIR"])
    new_settings["COARSE_SHAPE_OUTPUT_DIR"] = st.text_input("Coarse Shape Output Directory", value=settings["COARSE_SHAPE_OUTPUT_DIR"])
    new_settings["COARSE_SHAPE_OBJ_OUTPUT_NAME"] = st.text_input("Coarse Shape OBJ Output Name", value=settings["COARSE_SHAPE_OBJ_OUTPUT_NAME"])
    new_settings["COARSE_SHAPE_RENDERING_OUTPUT_DIR"] = st.text_input("Coarse Shape Rendering Output Directory", value=settings["COARSE_SHAPE_RENDERING_OUTPUT_DIR"])
    new_settings["IMPLICIT_AVATAR_OUTPUT_DIR"] = st.text_input("Implicit Avatar Output Directory", value=settings["IMPLICIT_AVATAR_OUTPUT_DIR"])
    new_settings["GENERATED_AVATAR_OUTPUT_DIR"] = st.text_input("Generated Avatar Output Directory", value=settings["GENERATED_AVATAR_OUTPUT_DIR"])
    new_settings["GENERATED_AVATAR_TEXTURE_OUTPUT_DIR"] = st.text_input("Generated Avatar Texture Output Directory", value=settings["GENERATED_AVATAR_TEXTURE_OUTPUT_DIR"])
    new_settings["GENERATED_AVATAR_FBX_OUTPUT_NAME"] = st.text_input("Generated Avatar FBX Output Name", value=settings["GENERATED_AVATAR_FBX_OUTPUT_NAME"])
    
    st.markdown("## Logging Settings:")
    new_settings["LOG_TO_FILE"] = st.checkbox("Log to File", value=settings["LOG_TO_FILE"])
    new_settings["LOGS_DIR"] = st.text_input("Logs Directory", value=settings["LOGS_DIR"])
    
    submit = st.form_submit_button("Save")

    if submit:
        new_settings["POSE_TYPE"] = "stand_pose" if pose_type == "Stand Pose" else "t_pose"
        save_settings(settings)
        st.success("Settings saved!")

reset_settings = st.button("Default Settings")
if reset_settings:
    with open("website/default_settings.yaml", "r") as f:
        default_settings = yaml.safe_load(f)
    save_settings(default_settings)
    st.success("Settings set to default!")
