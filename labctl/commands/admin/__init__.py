import typer
from .users import app as users_app
from .vpn import app as vpn_app
from .quota import app as quota_app

app = typer.Typer()

app.add_typer(users_app, name="users")
app.add_typer(vpn_app, name="vpn")
app.add_typer(quota_app, name="quota")
