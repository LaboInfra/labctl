from pathlib import Path

import yaml

CONFIG_LOCATION_DIR = f"{Path.home()}/.labctl/"
CONIIG_FILE = "config.yaml"

class Config:
    api_endpoint = None
    api_token = None
    token_type = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class ConfigNotInitialized(Exception):
    pass

class ConfigError(Exception):
    pass

class ConfigManager:

    config: Config = None

    def __init__(self, config: Config = None):
        """
        Args:
            config (Config, optional): new config object to save
        Raises:
            ConfigNotInitialized: When the config file is not found
            ConfigError: When there is an error loading the config file
        """
        if not Path(CONFIG_LOCATION_DIR).exists():
            Path(CONFIG_LOCATION_DIR).mkdir(parents=True)

        if config:
            self.config = config
            self.save()

        if not Path(CONFIG_LOCATION_DIR + CONIIG_FILE).exists():
            raise ConfigNotInitialized("Config file not found. Please run `labctl init` to initialize the config file.")
        try:
            self.load()
        except Exception:
            raise ConfigError("Error loading config file. Please run `labctl init` to reinitialize the config file.")

    def save(self):
        with open(CONFIG_LOCATION_DIR + CONIIG_FILE, "w") as f:
            yaml.dump(self.config.__dict__, f)

    def load(self):
        with open(CONFIG_LOCATION_DIR + CONIIG_FILE, "r") as f:
            self.config = Config()
            self.config.__dict__ = yaml.load(f, Loader=yaml.FullLoader)