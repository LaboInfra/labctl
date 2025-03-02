import typer

from rich.table import Table

from labctl.core import Config, APIDriver, console


app = typer.Typer()

@app.command(name="show")
def show():
    """
    Show the current configuration
    """
    config = Config()
    api_token = config.api_token
    if api_token:
        me = APIDriver().get("/me").json()
        # todo handle old token and valid token
        if me.get("email"):
            api_token = "Logged in as " + me["email"]
        else:
            api_token = "Token is invalid or expired (use `labctl login`)"
    else:
        api_token = "Not logged in"
    table = Table(title="Configuration")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("API URL", config.api_endpoint)
    table.add_row("API User", config.username)
    table.add_row("API Token", api_token)
    if config.admin_cli:
        table.add_row("Admin CLI Mode", "Enabled")
    console.print(table)

    if not config.api_endpoint:
        console.print("[red]Warning: API Endpoint not set. Use `labctl config set --api-endpoint=<server>` [/red]")
    if not config.api_token:
        console.print("[red]Warning: API Token not set. Use `labctl login`. [/red]")

@app.command(name="set")
def set_config(
    api_endpoint: str = typer.Option(None, help="Set the API endpoint"),
    username: str = typer.Option(None, help="Set the username"),
):
    """
    Set the configuration
    """
    new_config = {}
    if api_endpoint:
        new_config["api_endpoint"] = api_endpoint
    if username:
        new_config["username"] = username
    if not new_config:
        console.print("[red]No settings provided[/red]")
        raise typer.Abort()
    Config(**new_config).save()
    console.print("[green]Configuration updated[/green]")
    show()

@app.command(name="unset")
def unset_config(
    api_endpoint: bool = typer.Option(False, help="Unset the API endpoint")
):
    """
    Unset the configuration
    """
    new_config = {}
    if api_endpoint:
        new_config["api_endpoint"] = None
    if not new_config:
        console.print("[red]No settings provided[/red]")
        raise typer.Abort()
    Config(**new_config).save()
    console.print("[green]Configuration updated[/green]")
    show()
