from typer import Typer
from app.views.login import LoginView
from app.views.logout import LogoutView
from app.views.user import UserView

app = Typer()


@app.command()
def login(email: str, password: str = None):
    view = LoginView()
    view.dispatch(email=email, password=password)


@app.command()
def logout():
    view = LogoutView()
    view.dispatch()


app.add_typer(UserView().app, name="user")
