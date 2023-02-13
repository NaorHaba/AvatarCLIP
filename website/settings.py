import os
from enum import Enum
import time

import yaml

from website.config import Config


class POSE_TYPE(str, Enum):
    STAND_POSE = 'stand_pose'
    T_POSE = 't_pose'


class Settings:
    @staticmethod
    def load_settings():
        with open(Config.SETTING_YAML_PATH, "r") as f:
            return yaml.safe_load(f)

    @staticmethod
    def save_settings(settings):
        with open(Config.SETTING_YAML_PATH, "w") as f:
            yaml.dump(settings, f)

    @staticmethod
    def absolute_path(path):
        return os.path.join(os.path.dirname(__file__), os.pardir, path)

    settings = load_settings()
    LOG_FILE_NAME = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.log'


# TODO log the settings
# TODO when updating the settings, log the changes