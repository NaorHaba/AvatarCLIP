import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import argparse
import time

from website.config import Config
from website.logger import get_logger
from website.messages import Messages
from website.settings import Settings
from website.website_utils import absolute_path


settings = Settings()
logger = get_logger(__name__)

def run(coarse_shape_prompt: str):
    sys.path.append(absolute_path('AvatarGen/ShapeGen'))

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

    sys.path.remove(absolute_path('AvatarGen/ShapeGen'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--coarse_shape_prompt', type=str, required=True)
    parser.add_argument('--log_dir', type=str, default=time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
    parser.add_argument('--log_file_name', type=str, default='generate_coarse_shape.log')
    args = parser.parse_args()

    settings.settings['CURRENT_LOG_DIR'] = args.log_dir
    settings.settings['LOG_FILE_NAME'] = args.log_file_name

    run(args.coarse_shape_prompt)
