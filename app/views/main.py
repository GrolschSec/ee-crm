import typer
from app.controllers.main import AuthController, PermissionsController, UserController

app = typer.Typer()

def check_authentication():
    user = AuthController.is_authenticated()
    if not user[0]:
        typer.echo("You are not authenticated.")
        raise typer.Exit(1)
    return user[1]

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
        raise typer.Exit(1)

@app.command()
def useradd():
    user = check_authentication()
    if not PermissionsController.is_admin(user):
        typer.echo("You are not authorized to perform this action.")
        raise typer.Exit(1)
    fullname = typer.prompt("Enter the user full name")
    email = typer.prompt("Enter the user email")
    if UserController.verify_email(email):
        typer.echo("Error: email already exists.")
        raise typer.Exit(1)
    password = typer.prompt("Enter the user password", hide_input=True)
    role = typer.prompt("Enter the user role")


@app.command()
def test():
    user = check_authentication()
    typer.echo("You are authenticated.")
    if PermissionsController.is_admin(user):
        typer.echo("You are an admin.")
    elif PermissionsController.is_sales_user(user):
        typer.echo("You are a sales user.")
    elif PermissionsController.is_support_user(user):
        typer.echo("You are a support user.")
    elif PermissionsController.is_management_user(user):
        typer.echo("You are a management user.")
    else:
        typer.echo("You are an unknown user.")
