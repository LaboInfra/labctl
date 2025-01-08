import typer
from .users import app as users_app
from .vpn import app as vpn_app

app = typer.Typer()

app.add_typer(users_app, name="users")
app.add_typer(vpn_app, name="vpn")
