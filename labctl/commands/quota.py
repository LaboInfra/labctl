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

# labctl openstack quota add PROJECT_NAME QUOTATYPE VALUE
@cli_ready
@app.command(name="add")
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
@app.command(name="del")
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
