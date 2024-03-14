import typer
from app.controllers.main import AuthController

app = typer.Typer()

def check_authentication():
    if not AuthController.is_authenticated():
        typer.echo("You are not authenticated.")
        raise typer.Exit(1)

@app.command()
def login(email: str, password: str = None):
    if password is None:
        password = typer.prompt("Enter your password", hide_input=True)
    login = AuthController.login(email, password)
    if login["valid"]:
        if not AuthController.set_token():
            typer.echo("Error: failed to save token.")
            raise typer.Exit(1)
        typer.echo("Login successful.")
    else:
        typer.echo("Invalid credentials, please try again.")

@app.command()
def test():
    check_authentication()
    typer.echo("You are authenticated.")
