import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import argparse
import time

import torch
from pyhocon import ConfigFactory, HOCONConverter

from website.logger import get_logger
from website.messages import Messages
from website.settings import Settings
from website.website_utils import send_email

settings = Settings()
logger = get_logger(__name__)


def run(config_path, coarse_body_dir, is_continue=False):

    sys.path.append('AvatarGen/AppearanceGen')

    from AvatarGen.AppearanceGen.main import Runner

    output_folder = os.path.join(coarse_body_dir, settings.settings['IMPLICIT_AVATAR_OUTPUT_DIR'])
    render_folder = os.path.join(coarse_body_dir, settings.settings['COARSE_SHAPE_RENDERING_OUTPUT_DIR'])

    new_config_path = os.path.join(output_folder, 'config.conf')
    if not is_continue:
        # read config, change relevant parameters, and save to new config

        with open(config_path) as f:
            config = ConfigFactory.parse_string(f.read())

        config.put('general.base_exp_dir', output_folder)
        config.put('dataset.data_dir', render_folder)

        os.makedirs(output_folder, exist_ok=True)
        with open(new_config_path, 'w') as f:
            f.write(HOCONConverter().to_hocon(config))

        logger.info(Messages.NEW_CONFIG_FILE_INFO.format(new_config_path))

    logger.info(Messages.INITIALIZE_IMPLICIT_AVATAR_INFO.format(os.path.basename(coarse_body_dir)))
    runner = Runner(new_config_path, 'train', is_continue=is_continue)
    runner.train()
    logger.info(Messages.INITIALIZE_IMPLICIT_AVATAR_SUCCESS.format(os.path.basename(coarse_body_dir)))

    sys.path.remove('AvatarGen/AppearanceGen')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path', type=str, required=True)
    parser.add_argument('--coarse_body_dir', type=str, required=True)
    parser.add_argument('--is_continue', action='store_true')
    parser.add_argument('--log_dir', type=str, default=time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
    parser.add_argument('--log_file_name', type=str, default='initialize_implicit_avatar.log')
    args = parser.parse_args()

    settings.settings['CURRENT_LOG_DIR'] = args.log_dir
    settings.settings['LOG_FILE_NAME'] = args.log_file_name

    if torch.cuda.is_available():
        torch.set_default_tensor_type('torch.cuda.FloatTensor')
        logger.info(Messages.CUDA_DEFAULT_TENSOR_TYPE_INFO)

    try:
        run(args.config_path, args.coarse_body_dir, args.is_continue)

        if settings.settings['USER_EMAIL'] is not None:
            send_email(settings.settings['USER_EMAIL'], Messages.SUCCESS_EMAIL_BODY.format('initialize_implicit_avatar'), Messages.SUCCESS_EMAIL_BODY.format('initialize_implicit_avatar'))
    except Exception as e:
        logger.exception(e)
        if settings.settings['USER_EMAIL'] is not None:
            send_email(settings.settings['USER_EMAIL'], Messages.FAILURE_EMAIL_BODY.format('initialize_implicit_avatar', ''), Messages.FAILURE_EMAIL_BODY.format('initialize_implicit_avatar', str(e)))
