import typer

from labctl import __version__

app = typer.Typer()

@app.callback()
def callback():
    """
    labctl
    """


@app.command()
def version():
    """
    Print the version
    """
    version = __version__
    if version == "0.0.0":
        version = "dev"
    typer.echo("labctl version {}".format(version))
