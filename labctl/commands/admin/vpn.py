import typer

from rich.table import Table

from labctl.core import Config, APIDriver, console

app = typer.Typer()

app_group = typer.Typer()
app_acl = typer.Typer()
app_host = typer.Typer()

app.add_typer(app_group, name="group")
app.add_typer(app_acl, name="acl")
app.add_typer(app_host, name="host")

@app_group.command(name="add-user")
def add_user(username: str, group: str):
    """
    Add user to group
    """
    api_driver = APIDriver()
    rsp = api_driver.post(f"/users/{username}/vpn-group/{group}")
    if rsp.status_code >= 400:
        console.print(f"[red]Error: {rsp.text}[/red]")
        return
    console.print(f"User {username} added to group {group}")

@app_group.command(name="del-user")
def del_user(username: str, group: str):
    """
    Delete user from group
    """
    api_driver = APIDriver()
    rsp = api_driver.delete(f"/users/{username}/vpn-group/{group}")
    if rsp.status_code >= 400:
        console.print(f"[red]Error: {rsp.text}[/red]")
        return
    console.print(f"User {username} deleted from group {group}")

@app_acl.command(name="list")
def list_acls():
    """
    List VPN ACLs
    """
    api_driver = APIDriver()
    rsp = api_driver.get("/headscale/acls/")
    if rsp.status_code >= 400:
        console.print(f"[red]Error: {rsp.text}[/red]")
        return
    acls = rsp.json()
    table = Table(title="VPN ACLs")
    table.add_column("ID", style="cyan bold")
    table.add_column("Action", style="green")
    table.add_column("Source", style="magenta")
    table.add_column("Destination", style="yellow")
    table.add_column("Protocol", style="blue")

    for acl in acls:
        table.add_row(
            str(acl.get("id")),
            acl.get("action"),
            "\n".join(acl.get("src", [])),
            "\n".join(acl.get("dst", [])),
            acl.get("proto")
        )
    console.print(table)

@app_acl.command(name="add")
def add_acl(action: str, src: str, dst: str, proto: str = None):
    """
    Add VPN ACL
    """
    api_driver = APIDriver()
    data = {
        "action": action,
        "src": src.split(","),
        "dst": dst.split(","),
        "proto": proto
    }
    rsp = api_driver.post("/headscale/acls/", json=data)
    if rsp.status_code >= 400:
        console.print(f"[red]Error: {rsp.text}[/red]")
        return
    console.print("ACL added")

@app_acl.command(name="del")
def del_acl(acl_id: int):
    """
    Delete VPN ACL
    """
    api_driver = APIDriver()
    rsp = api_driver.delete(f"/headscale/acls/{acl_id}")
    if rsp.status_code >= 400:
        console.print(f"[red]Error: {rsp.text}[/red]")
        return
    console.print("ACL deleted")

@app_host.command(name="list")
def list_hosts():
    """
    List VPN hosts
    """
    api_driver = APIDriver()
    rsp = api_driver.get("/headscale/host/")
    if rsp.status_code >= 400:
        console.print(f"[red]Error: {rsp.text}[/red]")
        return
    hosts = rsp.json()
    table = Table(title="VPN Hosts IP -> Host binding")
    table.add_column("ID", style="cyan bold")
    table.add_column("Host", style="green")
    table.add_column("IP", style="magenta")

    for host in hosts:
        table.add_row(
            str(host.get("id")),
            host.get("name"),
            host.get("ip")
        )
    console.print(table)

@app_host.command(name="add")
def add_host(name: str, ip: str):
    """
    Add VPN host
    """
    api_driver = APIDriver()
    data = {
        "name": name,
        "ip": ip
    }
    rsp = api_driver.post("/headscale/host/", json=data)
    if rsp.status_code >= 400:
        console.print(f"[red]Error: {rsp.text}[/red]")
        return
    console.print("Host added")

@app_host.command(name="del")
def del_host(host_id: int):
    """
    Delete VPN host
    """
    api_driver = APIDriver()
    rsp = api_driver.delete(f"/headscale/host/{host_id}")
    if rsp.status_code >= 400:
        console.print(f"[red]Error: {rsp.text}[/red]")
        return
    console.print("Host deleted")