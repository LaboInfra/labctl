import typer

from rich.table import Table

from labctl.core import Config, APIDriver, console

app = typer.Typer()

@app.command(name="list")
def list():
    config = Config()
    users = APIDriver().get("/users/").json()
    table = Table(title=":adult: Users")
    print(users)
    table.add_column("Username", style="bold blue")
    table.add_column("Email", style="cyan")
    table.add_column("Disabled", style="yellow")
    table.add_column("Is Admin", style="red")

    for user in users:
        table.add_row(
            user["username"],
            user["email"],
            "Yes" if user["disabled"] else "No",
            "Yes" if user["is_admin"] else "No",
        )
    console.print(table)

@app.command(name="create")
def create(username: str, email: str):
    """
    Create a new user
    """
    api_driver = APIDriver()
    rsp = api_driver.post("/users/", json={"username": username, "email": email})
    if rsp.status_code >= 400:
        console.print(f"[red]Error: {rsp.text}[/red]")
        return
    console.print(f"User {username} created successfully")

@app.command(name="show")
def show(username: str):
    """
    Show the user details
    """
    user = APIDriver().get(f"/users/{username}").json()
    vpn_groups = APIDriver().get(f"/users/{username}/vpn-group").json()
    table = Table(title=":adult: User")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Username", user["username"])
    table.add_row("Email", user["email"])
    table.add_row("Disabled", "Yes" if user["disabled"] else "No")
    table.add_row("Is Admin", "Yes" if user["is_admin"] else "No")
    table.add_row("VPN Groups", ", ".join(vpn_groups.get("groups", [])))
    console.print(table)

@app.command(name="delete")
def delete(username: str, confirm: bool = typer.Option(False, "--confirm", help="Confirm the deletion")):
    """
    Delete a user
    """
    if not confirm:
        console.print("[red]Please confirm the deletion with --confirm[/red]")
        return
    rsp = APIDriver().delete(f"/users/{username}")
    if rsp.status_code >= 400:
        console.print(f"[red]Error: {rsp.text}[/red]")
        return
    console.print(f"User {username} deleted successfully")

@app.command(name="sync")
def sync():
    """
    Sync users from the directory
    """
    console.print("Todo")
