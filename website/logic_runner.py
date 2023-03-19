
import subprocess

from logic.generate_coarse_shape import run as generate_coarse_shape
from logic.render_coarse_shape import run as render_coarse_shape
from website.logger import get_logger
from website.messages import Messages
from website.settings import Settings
from website.website_utils import spinner, request_processed_info, absolute_path

settings = Settings()
logger = get_logger(__name__)


@spinner(Messages.GENERATE_NEW_COARSE_SHAPE_SPINNER_MESSAGE)
def run_generate_coarse_shape(shape_description):
    generate_coarse_shape(shape_description)
 

@spinner(Messages.RENDER_COARSE_SHAPE_SPINNER_MESSAGE)
def run_render_coarse_shape(path_to_obj_file):
    render_coarse_shape(path_to_obj_file)


@request_processed_info(settings.settings['USER_EMAIL'])
def run_initialize_implicit_avatar(implicit_config, path_to_render, is_continue):
    args = ['python', absolute_path('website/logic/initialize_implicit_avatar.py'), '--config_path', implicit_config, '--coarse_body_dir', path_to_render, '--log_dir', settings.settings['CURRENT_LOG_DIR']]
    if is_continue:
        args.append('--is_continue')
    run = subprocess.Popen(args, start_new_session=True)
    # save run.pid to log file
    logger.info(Messages.INITIALIZE_IMPLICIT_AVATAR_SUBPROCESS_INFO.format(run.pid))

@request_processed_info(settings.settings['USER_EMAIL'])
def run_generate_textures(texture_prompt, config_path, coarse_body_dir, avatar_name, is_continue):
    args = ['python', absolute_path('website/logic/generate_textures.py'), '--texture_prompt', texture_prompt, '--config_path', config_path, '--coarse_body_dir', coarse_body_dir, '--avatar_name', avatar_name, '--log_dir', settings.settings['CURRENT_LOG_DIR']]
    if is_continue:
        args.append('--is_continue')
    run = subprocess.Popen(args, start_new_session=True)
    # save run.pid to log file
    logger.info(Messages.GENERATE_TEXTURES_SUBPROCESS_INFO.format(run.pid))

@request_processed_info(settings.settings['USER_EMAIL'])
def run_convert_to_fbx(mesh_file, save_path):
    args = ['python', absolute_path('Avatar2FBX/export_fbx.py'), '--mesh_file', mesh_file, '--save_path', save_path, '--model_dir', absolute_path(settings.settings["SMPL_MODEL_DIR"])]
    run = subprocess.Popen(args, start_new_session=True)
    # save run.pid to log file
    logger.info(Messages.CONVERT_TO_FBX_SUBPROCESS_INFO.format(run.pid))


@request_processed_info(settings.settings['USER_EMAIL'])
def run_all(run_args):
    for avatar in run_args['run_args']:
        args = ['python', absolute_path('website/logic/run_all.py'), '--coarse_shape_prompt', avatar['coarse_shape_prompt'], '--texture_description_prompt', avatar['texture_description_prompt'], '--config_type', avatar['config_type'], '--log_dir', settings.settings['CURRENT_LOG_DIR'], '--log_file_name', settings.settings['LOG_FILE_NAME']]
        if avatar['should_continue']:
            args.append('--should_continue')
        if avatar['should_overwrite']:
            args.append('--should_overwrite')
        run = subprocess.Popen(args)
        # save run.pid to log file
        logger.info(Messages.RUN_ALL_SUBPROCESS_INFO.format(run.pid))