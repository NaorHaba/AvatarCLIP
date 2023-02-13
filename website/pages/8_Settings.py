import yaml
import streamlit as st

from website.config import Config
from website.messages import Messages
from website.settings import settings
from website.website_utils import spinner

st.set_page_config(layout="wide",
                   page_title=Messages.SETTINGS_PAGE_TITLE,
                   page_icon=Config.WEBSITE_ICON_PATH
                   )


placeholder = st.empty()
new_settings = dict()
with placeholder.form(key="settings_form", clear_on_submit=False):
    st.markdown(Messages.EMAIL_SETTINGS_HEADER)
    new_settings["USER_EMAIL"] = st.text_input("Email", value=settings.settings["USER_EMAIL"])

    st.markdown(Messages.MODEL_DIRECTORIES_HEADER)
    new_settings["SMPL_MODEL_DIR"] = st.text_input("SMPL Model Directory", value=settings.settings["SMPL_MODEL_DIR"])
    new_settings["VIRTUAL_AUTO_ENCODER_PATH"] = st.text_input("Virtual Auto Encoder Path", value=settings.settings["VIRTUAL_AUTO_ENCODER_PATH"])
    new_settings["CODEBOOK_PATH"] = st.text_input("Codebook Path", value=settings.settings["CODEBOOK_PATH"])
    new_settings["STAND_POSE_PATH"] = st.text_input("Stand Pose Path", value=settings.settings["STAND_POSE_PATH"])

    st.markdown(Messages.PROMPT_SETTINGS_HEADER)
    new_settings["ENHANCE_PROMPT"] = st.checkbox("Enhance Prompt", value=settings.settings["ENHANCE_PROMPT"])
    new_settings["PROMPT_ENHANCING"] = st.text_input("Prompt Enhancing", value=settings.settings["PROMPT_ENHANCING"])
    new_settings["FACE_PROMPT_WRAP"] = st.text_input("Face Prompt Wrap", value=settings.settings["FACE_PROMPT_WRAP"])
    new_settings["BACK_PROMPT_WRAP"] = st.text_input("Back Prompt Wrap", value=settings.settings["BACK_PROMPT_WRAP"])
    new_settings["NEUTRAL_BODY_SHAPE_PROMPT"] = st.text_input("Neutral Body Shape Prompt", value=settings.settings["NEUTRAL_BODY_SHAPE_PROMPT"])

    st.markdown(Messages.POSE_SETTINGS_HEADER)
    pose_type = st.radio("Pose Type", options=["Stand Pose", "T-Pose"], index=0 if settings.settings["POSE_TYPE"] == "stand_pose" else 1)

    st.markdown(Messages.IMPLICIT_AVATAR_INITIALIZATION_SETTINGS_HEADER)
    new_settings["SMALL_IMPLICIT_AVATAR_CONFIG"] = st.text_input("Small Implicit Avatar Config", value=settings.settings["SMALL_IMPLICIT_AVATAR_CONFIG"])
    new_settings["LARGE_IMPLICIT_AVATAR_CONFIG"] = st.text_input("Large Implicit Avatar Config", value=settings.settings["LARGE_IMPLICIT_AVATAR_CONFIG"])

    st.markdown(Messages.AVATAR_TEXTURE_SETTINGS_HEADER)
    new_settings["SMALL_AVATAR_TEXTURE_CONFIG"] = st.text_input("Small Avatar Texture Config", value=settings.settings["SMALL_AVATAR_TEXTURE_CONFIG"])
    new_settings["LARGE_AVATAR_TEXTURE_CONFIG"] = st.text_input("Large Avatar Texture Config", value=settings.settings["LARGE_AVATAR_TEXTURE_CONFIG"])

    st.markdown(Messages.OUTPUT_SETTINGS_HEADER)
    new_settings["OUTPUT_DIR"] = st.text_input("Output Directory", value=settings.settings["OUTPUT_DIR"])
    new_settings["COARSE_SHAPE_OUTPUT_DIR"] = st.text_input("Coarse Shape Output Directory", value=settings.settings["COARSE_SHAPE_OUTPUT_DIR"])
    new_settings["COARSE_SHAPE_OBJ_OUTPUT_NAME"] = st.text_input("Coarse Shape OBJ Output Name", value=settings.settings["COARSE_SHAPE_OBJ_OUTPUT_NAME"])
    new_settings["COARSE_SHAPE_RENDERING_OUTPUT_DIR"] = st.text_input("Coarse Shape Rendering Output Directory", value=settings.settings["COARSE_SHAPE_RENDERING_OUTPUT_DIR"])
    new_settings["IMPLICIT_AVATAR_OUTPUT_DIR"] = st.text_input("Implicit Avatar Output Directory", value=settings.settings["IMPLICIT_AVATAR_OUTPUT_DIR"])
    new_settings["GENERATED_AVATAR_OUTPUT_DIR"] = st.text_input("Generated Avatar Output Directory", value=settings.settings["GENERATED_AVATAR_OUTPUT_DIR"])
    new_settings["GENERATED_AVATAR_TEXTURE_OUTPUT_DIR"] = st.text_input("Generated Avatar Texture Output Directory", value=settings.settings["GENERATED_AVATAR_TEXTURE_OUTPUT_DIR"])
    new_settings["GENERATED_AVATAR_FBX_OUTPUT_NAME"] = st.text_input("Generated Avatar FBX Output Name", value=settings.settings["GENERATED_AVATAR_FBX_OUTPUT_NAME"])

    st.markdown(Messages.LOGGING_SETTINGS_HEADER)
    new_settings["LOG_TO_FILE"] = st.checkbox("Log to File", value=settings.settings["LOG_TO_FILE"])
    new_settings["LOGS_DIR"] = st.text_input("Logs Directory", value=settings.settings["LOGS_DIR"])

    submit = st.form_submit_button(Messages.SAVE_SETTINGS_FORM_SUBMIT_BUTTON)

    if submit:
        new_settings["POSE_TYPE"] = "stand_pose" if pose_type == "Stand Pose" else "t_pose"
        settings.save_settings()
        st.success(Messages.SETTINGS_SAVED_SUCCESSFULLY)


reset_settings = st.button(Messages.RESET_SETTINGS_BUTTON)
if reset_settings:
    with open(Config.DEFAULT_SETTINGS_YAML_PATH, "r") as f:
        default_settings = yaml.safe_load(f)
    settings.settings = default_settings
    settings.save_settings()
    st.success(Messages.SETTINGS_RESET_SUCCESSFULLY)
