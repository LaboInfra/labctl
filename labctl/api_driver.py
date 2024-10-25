import requests

from labctl.config import Config, ConfigManager

class APIDriver:

    api_url: str = None
    api_token: str = None
    headers: dict = None

    def __init__(self):
        config: Config = ConfigManager().config
        self.api_url = config.api_endpoint
        self.headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {config.api_token}'
        }

    def get(self, path: str):
        return requests.get(self.api_url + path, headers=self.headers).json()
