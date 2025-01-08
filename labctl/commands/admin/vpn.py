import typer

from rich.table import Table

from labctl.core import Config, APIDriver, console

app = typer.Typer()

app_group = typer.Typer()

app.add_typer(app_group, name="group")

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
