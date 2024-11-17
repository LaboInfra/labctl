from typing import Annotated
from time import sleep
from os import environ
from json import dumps

import requests
import typer
from rich.tree import Tree

from labctl import __version__, commands
from labctl.core import APIDriver, Config, console, cli_ready

app = typer.Typer()

app.add_typer(commands.config_app, name="config", help="Manage the configuration")
app.add_typer(commands.devices_app, name="devices", help="Manage vpn devices")

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
        version = "dev or installed from source"
    console.print(f"labctl version: {version} :rocket:")

@app.command()
@cli_ready
def me(
    json: bool = typer.Option(False, help="Output the data as json")
):
    """
    Print the current status of the fastonboard-api account
    """
    api_driver = APIDriver()
    data = api_driver.get("/me").json()
    if json:
        print(dumps(data))
        return
    tree = Tree("[bold blue]:open_file_folder: FastOnBoard Account[/bold blue]")
    tree.add("[bold]Username:[/bold] " + data.get("username"))
    tree.add("[bold]Email:[/bold] " + data.get("email"))

    devices_tree = tree.add(":open_file_folder: Devices")
    for device in data.get('devices_access', []):
        device_tree = devices_tree.add(":computer: " + device.get('name', ':question: Unnamed Device'))
        device_tree.add("[bold]ID:[/bold] " + device.get('id', ''))
        device_tree.add("[bold]IPv4:[/bold] " + device.get('ipv4', ''))
        device_tree.add("[bold]Latest Handshake:[/bold] " + str(device.get('latest_handshake', '')))
        device_tree.add("[bold]RX Bytes:[/bold] " + str(device.get('rx_bytes', 0)))
        device_tree.add("[bold]TX Bytes:[/bold] " + str(device.get('tx_bytes', 0)))
        device_tree.add("[bold]Remote IP:[/bold] " + str(device.get('remote_ip', '')))
    console.print(tree)


@app.command()
@cli_ready
def sync():
    """
    Ask FastOnBoard-API to sync your account onto the vpn and openstack services
    """
    api = APIDriver()
    me = api.get("/me").json()
    task_id = api.get("/users/" + me['username'] + "/sync").json()
    typer.echo(f"Syncing account for user {me['username']} this may take a while...")
    typer.echo("Task ID: " + task_id.get("id"))
    while True:
        task = api.get("/users/" + me['username'] + "/sync/" + task_id.get("id")).json()
        if task.get("status") == "SUCCESS":
            typer.echo("Sync successful")
            break
        if task.get("status") == "FAILURE":
            typer.echo("Sync failed")
            break
        sleep(1)

@app.command()
def login(username: str = typer.Option(None, help="The username to login with")):
    """
    Login to the FastOnBoard-API server
    Enter your password when prompted or set LABCTL_API_ENDPOINT_PASSWORD
    """
    env_user = environ.get("LABCTL_API_ENDPOINT_USERNAME")
    username = Config().username or username or env_user
    if not username:
        username = typer.prompt("Enter your username")

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
    }).json()
    if 'detail' in data:
        if "Method Not Allowed" in data['detail']:
            console.print("[red]Error: Invalid endpoint or path to api[/red]")
            return
        console.print(f"[red]Authentication failed : {data['detail']}[/red]")
        return
    if 'access_token' in data:
        config = Config()
        config.username=username
        config.api_token=data['access_token']
        config.token_type=data["token_type"]
        config.save()
        console.print("[green]Authentication successful[/green]")
        return
    console.print("[red]Authentication failed with unknown error[/red]")
    console.print_json(data)
