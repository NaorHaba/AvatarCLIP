import os
from enum import Enum
import time

import yaml

from website import website_utils
from website.config import Config


class POSE_TYPE(str, Enum):
    STAND_POSE = 'stand_pose'
    T_POSE = 't_pose'


class Settings:
    def __init__(self):
        self.settings = self.load_settings()
        self.settings['CURRENT_LOG_DIR'] = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        self.settings['LOG_FILE_NAME'] = 'main.log'
        os.makedirs(website_utils.absolute_path(os.path.join(self.settings['LOGS_DIR'], self.settings['CURRENT_LOG_DIR'])), exist_ok=True)

    @staticmethod
    def load_settings():
        with open(Config.SETTING_YAML_PATH, "r") as f:
            return yaml.safe_load(f)

    def save_settings(self):
        with open(Config.SETTING_YAML_PATH, "w") as f:
            yaml.dump(self.settings, f)


settings = Settings()


# TODO log the settings
# TODO when updating the settings, log the changes