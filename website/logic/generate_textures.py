import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import time

import torch
import argparse
from pyhocon import ConfigFactory, HOCONConverter

from website.logger import get_logger
from website.messages import Messages
from website.settings import Settings
from website.website_utils import absolute_path, send_email


settings = Settings()
logger = get_logger(__name__)

def run(texture_prompt, config_path, coarse_body_dir, avatar_name, is_continue=False):

    sys.path.append('AvatarGen/AppearanceGen')

    from AvatarGen.AppearanceGen.main import Runner

    output_folder = os.path.join(absolute_path(settings.settings['OUTPUT_DIR']), settings.settings['GENERATED_AVATAR_OUTPUT_DIR'], avatar_name, settings.settings["GENERATED_AVATAR_TEXTURE_OUTPUT_DIR"])

    new_config_path = os.path.join(output_folder, 'config.conf')

    if not is_continue:
        # read config, change relevant parameters, and save to new config

        with open(config_path) as f:
            config = ConfigFactory.parse_string(f.read())

        # get rendering obj and the last checkpoint of implicit avatar from coarse_body_dir
        coarse_obj_path = os.path.join(coarse_body_dir, settings.settings['COARSE_SHAPE_OBJ_OUTPUT_NAME'])

        checkpoint_dir = os.path.join(coarse_body_dir, settings.settings['IMPLICIT_AVATAR_OUTPUT_DIR'], 'checkpoints')
        last_checkpoint = sorted(os.listdir(checkpoint_dir))[-1]
        logger.info(Messages.LAST_CHECKPOINT_INFO.format(last_checkpoint))
        checkpoint_path = os.path.join(checkpoint_dir, last_checkpoint)

        render_dir = os.path.join(coarse_body_dir, 'render')

        config.put('general.base_exp_dir', output_folder)
        config.put('dataset.data_dir', render_dir)
        config.put('dataset.template_obj', coarse_obj_path)
        config.put('train.pretrain', checkpoint_path)
        config.put('clip.prompt', settings.settings['PROMPT_ENHANCING'].format(texture_prompt))
        config.put('clip.face_prompt', settings.settings['PROMPT_ENHANCING'].format(
            settings.settings['FACE_PROMPT_WRAP'].format(texture_prompt)))
        config.put('clip.back_prompt', settings.settings['PROMPT_ENHANCING'].format(
            settings.settings['BACK_PROMPT_WRAP'].format(texture_prompt)))

        os.makedirs(output_folder, exist_ok=True)
        with open(new_config_path, 'w') as f:
            f.write(HOCONConverter().to_hocon(config))

        logger.info(Messages.NEW_CONFIG_FILE_INFO.format(new_config_path))
    else:
        # use the existing config file
        if not os.path.exists(new_config_path):
            raise FileNotFoundError('No config file found in {}'.format(output_folder))

    logger.info(Messages.GENERATE_TEXTURES_INFO.format(os.path.basename(coarse_body_dir)))
    runner = Runner(new_config_path, 'train_clip', is_continue=is_continue)
    runner.init_clip()
    runner.init_smpl()
    runner.train_clip()
    logger.info(Messages.GENERATE_TEXTURES_SUCCESS.format(os.path.basename(coarse_body_dir)))

    sys.path.remove('AvatarGen/AppearanceGen')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--texture_prompt', type=str, required=True)
    parser.add_argument('--config_path', type=str, required=True)
    parser.add_argument('--coarse_body_dir', type=str, required=True)
    parser.add_argument('--avatar_name', type=str, required=True)
    parser.add_argument('--is_continue', action='store_true')
    parser.add_argument('--log_dir', type=str, default=time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
    parser.add_argument('--log_file_name', type=str, default='generate_textures.log')
    args = parser.parse_args()

    settings.settings['CURRENT_LOG_DIR'] = args.log_dir
    settings.settings['LOG_FILE_NAME'] = args.log_file_name

    if torch.cuda.is_available():
        torch.set_default_tensor_type('torch.cuda.FloatTensor')
        logger.info(Messages.CUDA_DEFAULT_TENSOR_TYPE_INFO)

    logger.info(Messages.GENERATE_TEXTURES_INFO.format(args.texture_prompt, args.coarse_body_dir))
    try:
        run(args.texture_prompt, args.config_path, args.coarse_body_dir, args.avatar_name, args.is_continue)
        if settings.settings['USER_EMAIL'] is not None:
            send_email(settings.settings['USER_EMAIL'], Messages.SUCCESS_EMAIL_BODY.format('generate_textures'), Messages.SUCCESS_EMAIL_BODY.format('generate_textures'))
    except Exception as e:
        logger.exception(e)
        if settings.settings['USER_EMAIL'] is not None:
            send_email(settings.settings['USER_EMAIL'], Messages.FAILURE_EMAIL_BODY.format('generate_textures', ''), Messages.FAILURE_EMAIL_BODY.format('generate_textures', str(e)))