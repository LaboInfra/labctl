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
        return self.get("/token/verify").json().get("valid", False)

    def get(self, path: str) -> requests.Response:
        return requests.get(self.api_url + path, headers=self.headers)

    def post(self, path: str, data: dict = {}, json: dict = {}, additional_headers: dict = {}) -> requests.Response:
        headers = self.headers
        headers.update(additional_headers)
        if data:
            return requests.post(self.api_url + path, headers=headers, data=data)
        if json:
            return requests.post(self.api_url + path, headers=headers, json=json)
        return requests.post(self.api_url + path, headers=headers)

    def delete(self, path: str) -> requests.Response:
        return requests.delete(self.api_url + path, headers=self.headers)
