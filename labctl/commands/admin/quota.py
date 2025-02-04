from typing import Optional
import typer

from rich.table import Table

from labctl.core import Config, APIDriver, console

app = typer.Typer()

@app.command(name="show")
def show_user(username: str):
    config = Config()
    api_driver = APIDriver()
    user_adjustements_list = api_driver.get(f"/quota/user/{username}/adjustements")
    if user_adjustements_list.status_code == 404:
        console.print(f"User {username} not found")
        return

    data_total = {}

    table_adjustements = Table(title="User quota adjustements")
    table_adjustements.add_column("ID", style="cyan")
    table_adjustements.add_column("Type", style="magenta")
    table_adjustements.add_column("Value", style="yellow")
    table_adjustements.add_column("Comment", style="green")

    for quota_adjustement in user_adjustements_list.json():
        table_adjustements.add_row(
            str(quota_adjustement["id"]),
            quota_adjustement["type"],
            str(quota_adjustement["quantity"]),
            quota_adjustement["comment"],
        )
        if quota_adjustement["type"] not in data_total:
            data_total[quota_adjustement["type"]] = 0
        data_total[quota_adjustement["type"]] += quota_adjustement["quantity"]

    console.print(table_adjustements)
    console.print("Total:")
    for key, value in data_total.items():
        console.print(f"  {key}: {value}")

@app.command(name="add")
def add_quota_adjustement(username: str, quota_type: str, quantity: int, comment: Optional[str] = None):
    payload = {
        "username": username,
        "type": quota_type,
        "quantity": quantity,
        "comment": comment,
    }
    rsp = APIDriver().post("/quota/adjust-user", json=payload)
    if rsp.status_code >= 400:
        console.print(f"[red]Error: {rsp.text}[/red]")
        return
    console.print(f"Adjustement added successfully")

@app.command(name="del")
def delete_quota_adjustement(adjustement_id: int, confirm: bool = typer.Option(False, "--confirm", help="Confirm the deletion")):
    # todo add confirmation with a get before to validate the information of this id
    if not confirm:
        console.print("Deletion not confirmed")
        return
    rsp = APIDriver().delete(f"/quota/adjust-user/{adjustement_id}")
    if rsp.status_code >= 400:
        console.print(f"[red]Error: {rsp.text}[/red]")
        return
    console.print(f"Adjustement deleted successfully")
