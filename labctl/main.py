from typing import Annotated
from time import sleep

import requests
import typer

from labctl import __version__, commands
from labctl.core import APIDriver, Config, console, cli_ready
from labctl.config import Config, ConfigManager

app = typer.Typer()
app.add_typer(commands.config_app, name="config", help="Manage the configuration")

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
def login(username: Annotated[str, typer.Argument(help="The username to authenticate with")]):
    """
    Login to the FastOnBoard-API server
    Enter your password when prompted or set LABCTL_API_ENDPOINT_PASSWORD
    """
    env_pass = environ.get("LABCTL_API_ENDPOINT_PASSWORD")
    if env_pass:
        password = env_pass
    else:
        password = typer.prompt("Enter your password", hide_input=True)

    api_driver = APIDriver()

    if not api_driver.api_url:
        console.print("[red]Error: API endpoint not set use `labctl config set --api-endpoint=<server>`[/red]")
        return

    data = api_driver.post("/token", data={
        'username': username,
        'password': password,
    }, additional_headers={
        'Content-Type': 'application/x-www-form-urlencoded',
    })
    if 'detail' in data:
        if "Method Not Allowed" in data['detail']:
            console.print("[red]Error: Invalid endpoint or path to api[/red]")
            return
        console.print(f"[red]Authentication failed : {data['detail']}[/red]")
        return
    if 'access_token' in data:
        config = Config()
        config.api_token=data['access_token']
        config.token_type=data["token_type"]
        config.save()
        console.print("[green]Authentication successful[/green]")
        return
    console.print("[red]Authentication failed with unknown error[/red]")
    console.print_json(data)
