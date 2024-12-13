from os import getcwd

import typer

from rich.table import Table

from labctl.core import Config, APIDriver, console
from labctl.core import cli_ready, wireguard

app = typer.Typer()

@app.command(name="list")
@cli_ready
def list_devices():
    """
    List devices
    """
    config = Config()
    devices = APIDriver().get("/devices/" + config.username).json()
    table = Table(title=":computer: Devices")
    table.add_column("ID", style="bold")
    table.add_column("Name", style="cyan")
    table.add_column("GivenName", style="magenta")
    table.add_column("IPv4", style="green")
    table.add_column("Created At", style="blue")
    table.add_column("Expires At", style="red")
    table.add_column("Last Seen", style="yellow")
    table.add_column("Online", style="green")

    for device in devices:
        table.add_row(
            device["id"],
            device["name"],
            device["givenName"],
            ", ".join(device["ipAddresses"]),
            device["createdAt"],
            device["expiry"],
            device["lastSeen"],
            "Yes" if device["online"] else "No",
        )
    console.print(table)

@app.command(name="create")
@cli_ready
def enroll(name: str = typer.Argument(..., help="The device name")):
    """
    Self enroll device to vpn
    """
    # Todo: Check if tailscale cli is installed and Create preauth key with api and call tailscale cli to enroll device
    ...

@app.command(name="delete")
@cli_ready
def quit():
    """
    Self logout or logout specified device
    """
    # Todo : Check if tailscale cli is installed logout user shutdown tailscale and call api to delete device if asked
    config = Config()