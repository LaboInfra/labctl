from functools import wraps

import typer
from labctl.core import APIDriver, Config, console

def cli_ready(func):
    """
    Decorator to check if the CLI is ready to be used
    Validates the configuration have been token and url set and check if token is still valid
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            config = Config()
            if not config.ready():
                console.print("[red]Configuration not ready, please run 'labctl config show' to check the current configuration[/red]")
                raise typer.Exit(1)
            api_driver = APIDriver()
            if not api_driver.validate_token():
                console.print("[red]Token is not valid, please run 'labctl config show' to check the current configuration[/red]")
                raise typer.Exit(1)
            return func(*args, **kwargs)
        except Exception as e:
            typer.echo(f"Error: {e}")
            raise typer.Exit(1)
    return wrapper
