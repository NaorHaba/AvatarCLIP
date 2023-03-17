import os
import sys
import time

import numpy as np
import torch
import argparse

from website.config import Config
from website.logger import get_logger
from website.messages import Messages
from website.settings import Settings, POSE_TYPE
from website.website_utils import absolute_path


settings = Settings()
logger = get_logger(__name__)

def run(obj_output_fname):
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--obj_output_fname', type=str, required=True)
    parser.add_argument('--log_dir', type=str, default=time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
    parser.add_argument('--log_file_name', type=str, default='render_coarse_shape.log')
    args = parser.parse_args()

    settings.settings['CURRENT_LOG_DIR'] = args.log_dir
    settings.settings['LOG_FILE_NAME'] = args.log_file_name

    run(args.obj_output_fname)
