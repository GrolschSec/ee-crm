from typer import Typer, prompt, echo, Exit
from app.controllers.user import UserController
from app.views.login import LoginView

app = Typer()


@app.command()
def login(email: str, password: str = None):
    view = LoginView()
    view.dispatch(email=email, password=password)


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
# def logout():
#     res = AuthController.delete_token_file()
#     if not res[0]:
#         echo(f"Error: {res[1]}")
#         raise Exit(1)
#     echo("Logout successful.")


@app.command()
def test():
    view = LoginView()
    view.dispatch()
