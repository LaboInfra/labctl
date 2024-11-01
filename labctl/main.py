from typing import Annotated
from time import sleep

import requests
import typer

from labctl import __version__
from labctl.api_driver import APIDriver
from labctl.config import Config, ConfigManager

app = typer.Typer()

@app.callback()
def callback():
    """
    labctl
    """

@app.command()
def version():
    """
    Print the version
    """
    version = __version__
    if version == "0.0.0":
        version = "dev"
    typer.echo("labctl version {}".format(version))

@app.command()
def status():
    """
    Print the current status of the fastonboard-api account
    """
    api = APIDriver()
    status: dict = api.me()
    typer.echo("Status:")
    typer.echo(f"  - User: {status['username']}")
    typer.echo(f"  - Email: {status['email']}")

@app.command()
def sync():
    """
    Ask FastOnBoard-API to sync your account onto the vpn and openstack services
    """
    api = APIDriver()
    me = api.me()
    task_id = api.get("/users/" + me['username'] + "/sync")
    typer.echo(f"Syncing account for user {me['username']} this may take a while...")
    typer.echo("Task ID: " + task_id.get("id"))
    while True:
        task = api.get("/users/" + me['username'] + "/sync/" + task_id.get("id"))
        if task.get("status") == "SUCCESS":
            typer.echo("Sync successful")
            break
        if task.get("status") == "FAILURE":
            typer.echo("Sync failed")
            break
        sleep(1)

@app.command()
def init(
    endpoint: Annotated[str, typer.Argument(help="The endpoint of the FastOnBoard-API server")],
    username: Annotated[str, typer.Argument(help="The username to authenticate with")],
    ):
    password = typer.prompt("Enter your password", hide_input=True)

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'username': username,
        'password': password,
    }
    data = requests.post(endpoint + "/token", headers=headers, data=data).json()
    if 'detail' in data:
        if "Method Not Allowed" in data['detail']:
            typer.echo("Invalid endpoint or path to api")
            return
        typer.echo(data['detail'])
        return
    if 'access_token' in data:
        typer.echo("Successfully authenticated")
        ConfigManager(
            Config(
                api_endpoint=endpoint,
                api_token=data['access_token'],
                token_type=data["token_type"]
            )
        )
        print("Config file initialized and authentication successful")
        return
    typer.echo("Authentication failed with unknown error")
