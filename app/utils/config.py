import json
import os


class Config:
    _config_data = {}

    @classmethod
    def load_config(cls):
        if not cls._config_data:
            config_path = os.path.join(os.path.dirname(__file__), "../../settings.json")

            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Config file {config_path} not found")

            with open(config_path, "r") as f:
                config_data = json.load(f)
                cls._config_data = config_data

            for key, value in cls._config_data.items():
                setattr(cls, key, value)


Config.load_config()
