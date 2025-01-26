from datetime import datetime
from os import getcwd
from shutil import which
from subprocess import run, PIPE

import typer

from rich.table import Table

from labctl.core import Config, APIDriver, console
from labctl.core import cli_ready

app = typer.Typer()

def parse_datetime(date_str: str) -> str:
    return datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")

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
    table.add_column("IPv4", style="green")
    table.add_column("Created At", style="blue")
    table.add_column("Expires At", style="red")
    table.add_column("Last Seen", style="yellow")
    table.add_column("Online", style="green")

    for device in devices:
        table.add_row(
            device["id"],
            device["givenName"],
            ", ".join(device["ipAddresses"]),
            parse_datetime(device["createdAt"]),
            (device["expiry"] if device["expiry"] != "0001-01-01T00:00:00Z" else "Never"),
            parse_datetime(device["lastSeen"]),
            "Yes" if device["online"] else "No",
        )
    console.print(table)

@app.command(name="enroll")
@cli_ready
def enroll():
    """
    Self enroll device to vpn
    """
    # Todo: Check if tailscale cli is installed and Create preauth key with api and call tailscale cli to enroll device
    bin = which("tailscale")
    if not bin:
        console.print("[red]TailScale cli not found in path please install it[/red]")
        return
    config = Config()
    api_driver = APIDriver()
    key_rsp = api_driver.get(f"/devices/{config.username}/preauthkey")
    key = key_rsp.json().get("key")
    print("Running tailscale login...")
    cmd = [bin, "login", "--login-server", "https://gw.laboinfra.net", "--auth-key", key, "--accept-routes"]
    print("Execeuting: " + " ".join(cmd))
    print("Output: " + run(cmd, stdout=PIPE).stdout.decode())

@app.command(name="logout")
def logout():
    """
    Self logout
    """
    bin = which("tailscale")
    if not bin:
        console.print("[red]TailScale cli not found in path please install it[/red]")
        return
    print("Running tailscale down...")
    print("Output: " + run([bin, "down"], stdout=PIPE).stdout.decode())
    print("Running tailscale logout...")
    print("Output: " + run([bin, "logout"], stdout=PIPE).stdout.decode())


@app.command(name="delete")
@cli_ready
def delete(
    name: str = typer.Argument(None, help="The device name (found on the list command)"),
):
    """
    Self logout or logout specified device
    """
    # Todo : Check if tailscale cli is installed logout user shutdown tailscale and call api to delete device if asked
    config = Config()
    api_driver = APIDriver()

    # delete http://localhost:8000/devices/admin/localhost-6uxdpldr
    status = api_driver.delete(f"/devices/{config.username}/{name}").json()

    # rsp "success": true, "msg": "Device deleted" }
    if status.get("success"):
        console.print(f"Device {name} has ben removed from the vpn server :fire:")
    else:
        console.print(f"Failed to remove device {name}")
        console.print(f"Reason given by the server : {status.get("msg")}")
