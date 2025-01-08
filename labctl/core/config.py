from pathlib import Path
from os import environ

import yaml

CONFIG_LOCATION_DIR = f"{Path.home()}/"
CONFIG_FILE = environ.get("LABCTL_CONFIG_FILE", ".labctl.yaml")

class Config:

    api_endpoint: str
    username: str
    api_token: str
    token_type: str
    admin_cli: bool = False

    def __init__(self, **kwargs):
        """
        Initialize the configuration object
        The kwargs are used to update the configuration on fly like so:
        config = Config(api_endpoint="http://localhost:8000").save()
        """
        if not Path(CONFIG_LOCATION_DIR).exists():
            Path(CONFIG_LOCATION_DIR).mkdir(parents=True)

        # If the config file does not exist, create a new one else load the existing one
        if not Path(CONFIG_LOCATION_DIR + CONFIG_FILE).exists():
            self.save()
        else:
            self.load()
        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        """
        Get the value of the attribute or return None if it does not exist
        """
        return self.__dict__.get(name, None)

    def save(self):
        """
        Save the current configuration to the configuration file
        """
        with open(CONFIG_LOCATION_DIR + CONFIG_FILE, "w") as stream:
            yaml.dump(self.__dict__, stream)
        return self

    def load(self):
        """
        Load the configuration from the configuration file
        """
        with open(CONFIG_LOCATION_DIR + CONFIG_FILE, "r") as stream:
            self.__dict__.update(yaml.load(stream, Loader=yaml.FullLoader))
        return self

    def ready(self):
        """
        Check if the configuration is ready to be used
        """
        return all([self.api_endpoint, self.api_token, self.token_type, self.username])
