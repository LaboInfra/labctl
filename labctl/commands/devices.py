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
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("IPv4", style="green")
    table.add_column("RX Bytes", style="blue")
    table.add_column("TX Bytes", style="yellow")
    table.add_column("Remote IP", style="red")

    for device in devices:
        table.add_row(
            device["id"],
            device["name"],
            device["ipv4"],
            device["rx_bytes"],
            device["tx_bytes"],
            device["remote_ip"],
        )
    console.print(table)

@app.command(name="create")
@cli_ready
def create_device(name: str = typer.Argument(..., help="The device name")):
    """
    Create a device
    """
    rsp = APIDriver().post(
        f"/devices/{Config().username}",
        json={"name": name},
        additional_headers={"Content-Type": "application/json"}
    )
    if rsp.status_code >= 200 < 300:
        console.print(f"Device {name} created :tada:")
        data = rsp.json()
        config_path = f"/{getcwd()}/{name}.conf"
        wireguard.generate_config(data["device"], data["private_key"], config_path)
        console.print(f"Configuration file saved to {config_path}")
        return
    console.print(f"Error creating device {name} ({rsp.status_code})")

@app.command(name="delete")
@cli_ready
def delete_device(
    device_id: str = typer.Argument(..., help="The device ID")
):
    """
    Delete a device
    """
    rsp = APIDriver().delete(f"/devices/{Config().username}/{device_id}")
    if rsp.status_code == 200:
        console.print(f"Device {device_id} deleted :fire:")
        return
    console.print(f"Error deleting device {device_id} ({rsp.status_code})")
