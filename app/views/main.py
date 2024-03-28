from typer import Typer, prompt, echo, Exit
from app.controllers.authentication import AuthController
from app.controllers.user import UserController
from app.views.utils import user_creation, check_authentication

app = Typer()


@app.command()
def login(email: str, password: str = None):
    if password is None:
        password = prompt("Enter your password", hide_input=True)
    login = AuthController.login(email, password)
    if login["valid"]:
        if not AuthController.write_token_to_file():
            echo("Error: failed to save token.")
            raise Exit(1)
        echo("Login successful.")
    else:
        echo("Invalid credentials, please try again.")
        raise Exit(1)


@app.command()
def useradd(admin: bool = False):
    if admin:
        if UserController.admin_exist():
            echo("Admin user already exists.")
            raise Exit(1)
        user_creation(admin=True)
    else:
        user = check_authentication()
        role = user.role.name
        if role == "admin" or role == "management":
            user_creation()
        else:
            echo("You do not have permission to create a user.")
            raise Exit(1)


# @app.command()
# def test():
#     user = check_authentication()
#     typer.echo("You are authenticated.")
#     if PermissionsController.is_admin(user):
#         typer.echo("You are an admin.")
#     elif PermissionsController.is_sales_user(user):
#         typer.echo("You are a sales user.")
#     elif PermissionsController.is_support_user(user):
#         typer.echo("You are a support user.")
#     elif PermissionsController.is_management_user(user):
#         typer.echo("You are a management user.")
#     else:
#         typer.echo("You are an unknown user.")
