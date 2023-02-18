
import subprocess

from logic.generate_coarse_shape import run as generate_coarse_shape
from logic.render_coarse_shape import run as render_coarse_shape
from website.logger import get_logger
from website.messages import Messages
from website.settings import settings
from website.website_utils import spinner, request_processed_info, absolute_path

logger = get_logger(__name__)


@spinner(Messages.GENERATE_NEW_COARSE_SHAPE_SPINNER_MESSAGE)
def run_generate_coarse_shape(shape_description):
    generate_coarse_shape(shape_description)
 

@spinner(Messages.RENDER_COARSE_SHAPE_SPINNER_MESSAGE)
def run_render_coarse_shape(path_to_obj_file):
    render_coarse_shape(path_to_obj_file)


@request_processed_info(settings.settings['USER_EMAIL'])
def run_initialize_implicit_avatar(implicit_config, path_to_render, is_continue):
    run = subprocess.Popen(['python', absolute_path('logic/initialize_implicit_avatar.py'), implicit_config, path_to_render, str(is_continue), settings.settings['CURRENT_LOG_DIR']])
    # save run.pid to log file
    logger.info(Messages.INITIALIZE_IMPLICIT_AVATAR_SUBPROCESS_INFO.format(run.pid))


@request_processed_info(settings.settings['USER_EMAIL'])
def run_generate_textures(texture_prompt, config_path, coarse_body_dir, is_continue):
    run = subprocess.Popen(['python', absolute_path('logic/generate_textures.py'), texture_prompt, config_path, coarse_body_dir, str(is_continue), settings.settings['CURRENT_LOG_DIR']])
    # save run.pid to log file
    logger.info(Messages.GENERATE_TEXTURES_SUBPROCESS_INFO.format(run.pid))


@request_processed_info(settings.settings['USER_EMAIL'])
def run_all(run_args):
    for avatar in run_args.values():
        run = subprocess.Popen(['python', absolute_path('logic/run_all.py'), avatar['coarse_shape_prompt'], avatar['texture_description_prompt'], str(avatar['should_continue']), str(avatar['should_overwrite']), avatar['config_type'], settings.settings['CURRENT_LOG_DIR'], settings.settings['LOG_FILE_NAME']])
        # save run.pid to log file
        logger.info(Messages.RUN_ALL_SUBPROCESS_INFO.format(run.pid))