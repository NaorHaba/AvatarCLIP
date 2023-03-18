import os
import sys
import argparse
import time

import torch
from pyhocon import ConfigFactory, HOCONConverter

from website.logger import get_logger
from website.messages import Messages
from website.settings import Settings
from website.website_utils import send_email, absolute_path

from website.logic.generate_coarse_shape import run as generate_coarse_shape
from website.logic.render_coarse_shape import run as render_coarse_shape
from website.logic.initialize_implicit_avatar import run as initialize_implicit_avatar
from website.logic.generate_textures import run as generate_textures
from Avatar2FBX.export_fbx import run as convert_to_fbx


settings = Settings()
logger = get_logger(__name__)


def run(coarse_shape_prompt, texture_description_prompt, config_type, should_continue=False, should_overwrite=False):
    generate_coarse_shape(coarse_shape_prompt)
    
    obj_output_fname = absolute_path(os.path.join(coarse_shape_prompt, settings.settings['COARSE_SHAPE_OBJ_OUTPUT_NAME']))
    
    render_coarse_shape(obj_output_fname)

    if config_type == 'small':
        implicit_config_path = settings.settings.SMALL_IMPLICIT_AVATAR_CONFIG
        avatar_texture_config_path = settings.settings.SMALL_AVATAR_TEXTURE_CONFIG
    else:
        implicit_config_path = settings.settings.LARGE_IMPLICIT_AVATAR_CONFIG
        avatar_texture_config_path = settings.settings.LARGE_AVATAR_TEXTURE_CONFIG

    coarse_output_folder = absolute_path(os.path.join(settings.settings['OUTPUT_DIR'], settings.settings['COARSE_SHAPE_OUTPUT_DIR']))
    coarse_body_dir = absolute_path(os.path.join(coarse_output_folder, coarse_shape_prompt))

    if should_overwrite:
        continue_flag = False
    elif should_continue:
        continue_flag = True
    else:
        continue_flag = False

    initialize_implicit_avatar(implicit_config_path, coarse_body_dir, continue_flag)

    avatar_name = f"{texture_description_prompt} ({coarse_shape_prompt})"

    generate_textures(texture_description_prompt, avatar_texture_config_path, coarse_body_dir, avatar_name, continue_flag)

    avatar_output_folder = absolute_path(os.path.join(settings.settings['OUTPUT_DIR'], settings.settings['GENERATED_AVATAR_OUTPUT_DIR']))
    selected_avatar_dir_path = os.path.join(avatar_output_folder, avatar_name)
    save_path = os.path.join(selected_avatar_dir_path, settings.settings['GENERATED_AVATAR_FBX_OUTPUT_NAME'])
    avatar_dir_path = os.path.join(avatar_output_folder, avatar_name)
    texture_folder = os.path.join(avatar_dir_path, settings.settings['GENERATED_AVATAR_TEXTURE_OUTPUT_DIR'])
    meshes_folder = os.path.join(texture_folder, "meshes")
    mesh_file = os.path.join(meshes_folder, sorted(os.listdir(meshes_folder))[-1])
    model_dir = absolute_path(settings.settings["SMPL_MODEL_DIR"])
    convert_to_fbx(mesh_file, save_path, model_dir)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--coarse_shape_prompt', type=str, required=True)
    parser.add_argument('--texture_description_prompt', type=str, required=True)
    parser.add_argument('--config_type', type=str, required=True)
    parser.add_argument('--should_continue', action='store_true')
    parser.add_argument('--should_overwrite', action='store_true')
    parser.add_argument('--log_dir', type=str, default=time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
    parser.add_argument('--log_file_name', type=str, default='initialize_implicit_avatar.log')
    args = parser.parse_args()

    settings.settings['CURRENT_LOG_DIR'] = args.log_dir
    settings.settings['LOG_FILE_NAME'] = args.log_file_name

    if torch.cuda.is_available():
        torch.set_default_tensor_type('torch.cuda.FloatTensor')
        logger.info(Messages.CUDA_DEFAULT_TENSOR_TYPE_INFO)

    try:
        run(args.coarse_shape_prompt, args.texture_description_prompt, args.should_continue, args.should_overwrite, args.config_type)
        
        if settings.settings.USER_EMAIL is not None:
            send_email(settings.settings.USER_EMAIL, Messages.SUCCESS_EMAIL_BODY.format('initialize_implicit_avatar'), Messages.SUCCESS_EMAIL_BODY.format('initialize_implicit_avatar'))
    except Exception as e:
        logger.exception(e)
        if settings.settings.USER_EMAIL is not None:
            send_email(settings.settings.USER_EMAIL, Messages.FAILURE_EMAIL_BODY.format('initialize_implicit_avatar'), Messages.FAILURE_EMAIL_BODY.format('initialize_implicit_avatar', str(e)))
