from typing import Optional
from typer import Typer
from labctl.core import cli_ready, Config, APIDriver, console
from rich.table import Table

app = Typer()

@cli_ready
@app.command(name="show-project")
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

@cli_ready
@app.command(name="set")
def set_quota(project: str, quota_type: str, quantity: int, comment: Optional[str] = None):
    """
    Add quota to OpenStack project
    """
    config = Config()
    console.print(f"[cyan]Setting {quota_type}={quantity} to OpenStack project {project}[/cyan]")
    payload = {
        "username": config.username,
        "project_name": project,
        "type": quota_type,
        "quantity": quantity,
        "comment": comment
    }
    call = APIDriver().put(f"/quota/adjust-project", json=payload)
    if call.status_code >= 400:
        console.print(f"[red]Error: {call.text}[/red]")
        return
    console.print(f"[green]Quota {quota_type}={quantity} set to project {project}[/green]")

@cli_ready
@app.command(name="unset")
def unset_quota(project: str, quota_type: str):
    """
    Add quota to OpenStack project
    """
    config = Config()
    console.print(f"[cyan]Unsetting {quota_type} to OpenStack project {project}[/cyan]")
    payload = {
        "username": config.username,
        "project_name": project,
        "type": quota_type,
        "quantity": 0,
        "comment": ""
    }
    call = APIDriver().put(f"/quota/adjust-project", json=payload)
    if call.status_code >= 400:
        console.print(f"[red]Error: {call.text}[/red]")
        return
    console.print(f"[green]Quota {quota_type} unset from project {project}[/green]")
