import os

from website.utils import POSE_TYPE


class Settings:
    SMPL_MODEL_DIR = 'smpl_models/'

    VIRTUAL_AUTO_ENCODER_PATH = 'AvatarGen/ShapeGen/data/model_VAE_16.pth'
    CODEBOOK_PATH = 'AvatarGen/ShapeGen/data/codebook.pth'
    STAND_POSE_PATH = 'AvatarGen/ShapeGen/stand_pose.npy'

    ENHANCE_PROMPT = True
    PROMPT_ENHANCING = 'a 3d rendering of {} in unreal engine'
    FACE_PROMPT_WRAP = 'the face of {}'
    BACK_PROMPT_WRAP = 'the back of {}'
    NEUTRAL_BODY_SHAPE_PROMPT = 'person'  # 'man' / 'woman'

    # coarse body shape rendering
    POSE_TYPE = POSE_TYPE.STAND_POSE

    # appearance rendering
    SMALL_IMPLICIT_AVATAR_CONFIG = 'AvatarGen/AppearanceGen/confs/general_confs/small_implicit_avatar.conf'
    LARGE_IMPLICIT_AVATAR_CONFIG = 'AvatarGen/AppearanceGen/confs/general_confs/large_implicit_avatar.conf'

    SMALL_AVATAR_TEXTURE_CONFIG = 'AvatarGen/AppearanceGen/confs/general_confs/small_avatar_texture.conf'
    LARGE_AVATAR_TEXTURE_CONFIG = 'AvatarGen/AppearanceGen/confs/general_confs/large_avatar_texture.conf'

    OUTPUT_DIR = 'output/'
    COARSE_SHAPE_OUTPUT_DIR = 'coarse_shape/'
    COARSE_SHAPE_OBJ_OUTPUT_NAME = 'coarse_shape.obj'
    COARSE_SHAPE_RENDERING_OUTPUT_DIR = 'render/'
    IMPLICIT_AVATAR_OUTPUT_DIR = 'implicit_avatar/'

    GENERATED_AVATAR_OUTPUT_DIR = 'generated_avatar/'
    GENERATED_AVATAR_TEXTURE_OUTPUT_DIR = 'texture/'
    GENERATED_AVATAR_FBX_OUTPUT_NAME = 'avatar.fbx'

    @staticmethod
    def absolute_path(path):
        return os.path.join(os.path.dirname(__file__), path)
