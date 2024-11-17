import requests
import typer
from labctl import __version__
from labctl.core import Config


class APIDriver:

    api_url: str = None
    api_token: str = None
    headers: dict = None

    def __init__(self):
        config: Config = Config()
        self.api_url = config.api_endpoint
        if self.api_url.endswith("/"):
            self.api_url = self.api_url.rstrip("/")
        self.headers = {
            'accept': 'application/json',
            'User-Agent': 'labctl/' + __version__,
            'Authorization': f'Bearer {config.api_token}'
        }

    def validate_token(self):
        return self.get("/token/verify").get("valid", False)

    def get(self, path: str):
        return requests.get(self.api_url + path, headers=self.headers).json()

    def post(self, path: str, data: dict = {}, additional_headers: dict = {}):
        headers = self.headers
        headers.update(additional_headers)
        return requests.post(self.api_url + path, headers=headers, data=data).json()
