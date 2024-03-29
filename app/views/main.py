from typer import Typer
from app.views.login import LoginView
from app.views.useradd import UserAddAdminView, UserAddUserView

app = Typer()


@app.command()
def login(email: str, password: str = None):
    view = LoginView()
    view.dispatch(email=email, password=password)


@app.command()
def useradd(admin: bool = False):
    if admin:
        UserAddAdminView().dispatch()
    else:
        UserAddUserView().dispatch()


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
