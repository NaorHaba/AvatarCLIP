import os
import sys

import numpy as np
import torch
from pyhocon import ConfigFactory, HOCONConverter

from website.config import Config
from website.messages import Messages
from website.settings import settings, POSE_TYPE
from website.website_utils import absolute_path
from website.logger import get_logger

logger = get_logger(__name__)


if torch.cuda.is_available():
    torch.set_default_tensor_type('torch.cuda.FloatTensor')
    logger.info(Messages.CUDA_DEFAULT_TENSOR_TYPE_INFO)


def generate_coarse_shape(coarse_shape_prompt: str):
    sys.path.append('AvatarGen/ShapeGen')

    from AvatarGen.ShapeGen.main import shape_gen
    from AvatarGen.ShapeGen.utils import writeOBJ

    output_folder = os.path.join(absolute_path(settings.settings['OUTPUT_DIR']), settings.settings['COARSE_SHAPE_OUTPUT_DIR'], coarse_shape_prompt)

    smpl_args = {
        'model_folder': absolute_path(settings.settings['SMPL_MODEL_DIR']),
        'model_type': Config.SMPL_MODEL_TYPE,
        'gender': Config.SMPL_GENDER,
        'num_betas': Config.SMPL_NUM_BETAS
    }

    neutral_body_shape = settings.settings['NEUTRAL_BODY_SHAPE_PROMPT']
    if settings.settings['ENHANCE_PROMPT']:
        coarse_shape_prompt = settings.settings['PROMPT_ENHANCING'].format(coarse_shape_prompt)
        neutral_body_shape = settings.settings['PROMPT_ENHANCING'].format(neutral_body_shape)
    logger.info(Messages.GENERATE_NEW_COARSE_SHAPE_INFO.format(coarse_shape_prompt))
    v, f, zero_beta_v = shape_gen(smpl_args,
                                  absolute_path(settings.settings['VIRTUAL_AUTO_ENCODER_PATH']),
                                  absolute_path(settings.settings['CODEBOOK_PATH']),
                                  neutral_body_shape,
                                  coarse_shape_prompt)

    os.makedirs(output_folder, exist_ok=True)
    obj_output_fname = os.path.join(output_folder, settings.settings['COARSE_SHAPE_OBJ_OUTPUT_NAME'])
    writeOBJ(obj_output_fname, v, f)

    logger.info(Messages.GENERATE_NEW_COARSE_SHAPE_SUCCESS.format(obj_output_fname))

    sys.path.remove('AvatarGen/ShapeGen')


def render_coarse_shape_wrapper(obj_output_fname):
    sys.path.append('AvatarGen/ShapeGen')

    from AvatarGen.ShapeGen.render import render_coarse_shape
    from AvatarGen.ShapeGen.utils import readOBJ

    output_folder = os.path.dirname(obj_output_fname)

    smpl_args = {
        'model_folder': absolute_path(settings.settings['SMPL_MODEL_DIR']),
        'model_type': Config.SMPL_MODEL_TYPE,
        'gender': Config.SMPL_GENDER,
        'num_betas': Config.SMPL_NUM_BETAS
    }

    render_output_folder = os.path.join(output_folder, settings.settings['COARSE_SHAPE_RENDERING_OUTPUT_DIR'])

    if settings.settings['POSE_TYPE'] == POSE_TYPE.STAND_POSE:
        pose = np.load(absolute_path(settings.settings['STAND_POSE_PATH']))
    elif settings.settings['POSE_TYPE'] == POSE_TYPE.T_POSE:
        pose = np.zeros([1, 24, 3], dtype=np.float32)
        pose[:, 0, 0] = np.pi / 2
    else:
        raise NotImplementedError

    v_shaped, _, _, _ = readOBJ(obj_output_fname)
    v_shaped = torch.from_numpy(v_shaped.astype(np.float32)).reshape(1, -1, 3).cuda()

    logger.info(Messages.RENDER_COARSE_SHAPE_INFO.format(obj_output_fname))
    render_coarse_shape(pose, v_shaped, smpl_args, render_output_folder)
    logger.info(Messages.RENDER_COARSE_SHAPE_SUCCESS.format(render_output_folder))

    sys.path.remove('AvatarGen/ShapeGen')


def initialize_implicit_avatar(config_path, coarse_body_dir, is_continue=False):

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


def generate_textures(texture_prompt, config_path, coarse_body_dir, is_continue=False):

    sys.path.append('AvatarGen/AppearanceGen')

    from AvatarGen.AppearanceGen.main import Runner

    output_folder = os.path.join(absolute_path(settings.settings['OUTPUT_DIR']), settings.settings['GENERATED_AVATAR_OUTPUT_DIR'], texture_prompt)

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


def convert_to_FBX():
    pass
