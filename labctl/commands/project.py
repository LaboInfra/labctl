from typer import Typer
from labctl.core import cli_ready, Config, APIDriver, console
from rich.table import Table

app = Typer()

@cli_ready
@app.command(name="list")
def list_projects():
    """
    List OpenStack projects
    """
    config = Config()
    console.print("[cyan]Listing OpenStack projects[/cyan]")
    call = APIDriver().get(f"/openstack/projects/{config.username}")
    if call.status_code >= 400:
        console.print(f"[red]Error: {call.text}[/red]")
        return
    table = Table(title="Projects")
    table.add_column("Id")
    table.add_column("Name")
    for project in call.json():
        table.add_row(str(project['id']), project['name'])
    console.print(table)

@cli_ready
@app.command(name="create")
def create_project(name: str):
    """
    Create OpenStack project
    """
    config = Config()
    console.print(f"[cyan]Creating OpenStack project {name}[/cyan]")
    call = APIDriver().post(f"/openstack/projects/{name}")
    if call.status_code >= 400:
        console.print(f"[red]Error: {call.text}[/red]")
        return
    console.print(f"[green]Project {name} created[/green]")

@cli_ready
@app.command(name="delete")
def delete_project(name: str):
    """
    Delete OpenStack project
    """
    config = Config()
    console.print(f"[cyan]Deleting OpenStack project {name}[/cyan]")
    call = APIDriver().delete(f"/openstack/projects/{name}")
    if call.status_code >= 400:
        console.print(f"[red]Error: {call.text}[/red]")
        return
    console.print(f"[green]Project {name} deleted[/green]")

@cli_ready
@app.command(name="add-user")
def add_user(project: str, user: str):
    """
    Add user to OpenStack project
    """
    console.print(f"[cyan]Adding user {user} to OpenStack project {project}[/cyan]")
    call = APIDriver().put(f"/openstack/projects/{project}/users/{user}")
    if call.status_code >= 400:
        console.print(f"[red]Error: {call.text}[/red]")
        return
    console.print(f"[green]User {user} added to project {project}[/green]")

@cli_ready
@app.command(name="del-user")
def del_user(project: str, user: str):
    """
    Delete user from OpenStack project
    """
    config = Config()
    console.print(f"[cyan]Deleting user {user} from OpenStack project {project}[/cyan]")
    call = APIDriver().delete(f"/openstack/projects/{project}/users/{user}")
    if call.status_code >= 400:
        console.print(f"[red]Error: {call.text}[/red]")
        return
    console.print(f"[green]User {user} deleted from project {project}[/green]")
