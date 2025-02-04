from typing import Optional
from typer import Typer
from labctl.core import cli_ready, Config, APIDriver, console
from rich.table import Table

app = Typer()
project = Typer()
quota = Typer()

app.add_typer(project, name="project")
app.add_typer(quota, name="quota")

@cli_ready
@app.command(name="reset-password")
def reset_password():
    """
    Reset OpenStack password
    """
    console.print("[cyan]Resetting your OpenStack user password[/cyan]")
    config = Config()
    call = APIDriver().put(f"/openstack/users/{config.username}/reset-password")
    if call.status_code >= 400:
        console.print(f"[red]Error: {call.text}[/red]")
        return
    console.print(f"[green]New password for {config.username} is [/green][bright_yellow]{call.json()['password']}[/bright_yellow]")
    console.print("[yellow]Please change it after login on console[/yellow]")

@cli_ready
@project.command(name="list")
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
@project.command(name="create")
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
@project.command(name="delete")
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
@project.command(name="add-user")
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
@project.command(name="del-user")
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

# quota
@cli_ready
@quota.command(name="show-project")
def show_project_quota(project: str):
    """
    List OpenStack project quota
    """
    call = APIDriver().get(f"/quota/project/{project}/adjustements")
    if call.status_code >= 400:
        console.print(f"[red]Error: {call.text}[/red]")
        return
    table = Table(title="Quotas for project " + project)

    table.add_column("Id")
    table.add_column("Type")
    table.add_column("Quantity")
    table.add_column("User")
    table.add_column("Comment")

    for quota in call.json():
        table.add_row(str(quota['id']), quota['type'], str(quota['quantity']), quota['username'], quota['comment'])

    console.print(table)

# labctl openstack quota add PROJECT_NAME QUOTATYPE VALUE
@cli_ready
@quota.command(name="add")
def add_quota(project: str, quota_type: str, quantity: int, comment: Optional[str] = None):
    """
    Add quota to OpenStack project
    """
    config = Config()
    console.print(f"[cyan]Adding {quota_type}={quantity} to OpenStack project {project}[/cyan]")
    payload = {
        "username": config.username,
        "project_name": project,
        "type": quota_type,
        "quantity": quantity,
        "comment": comment
    }
    call = APIDriver().post(f"/quota/adjust-project", json=payload)
    if call.status_code >= 400:
        console.print(f"[red]Error: {call.text}[/red]")
        return
    console.print(f"[green]Quota {quota_type}={quantity} added to project {project}[/green]")

@cli_ready
@quota.command(name="del")
def del_quota(id: int):
    """
    Delete quota from OpenStack project
    """
    console.print(f"[cyan]Deleting quota {id} from OpenStack project[/cyan]")
    call = APIDriver().delete(f"/quota/adjust-project/{id}/{Config().username}")
    if call.status_code >= 400:
        console.print(f"[red]Error: {call.text}[/red]")
        return
    console.print(f"[green]Quota {id} deleted from project[/green]")
