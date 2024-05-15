from typer import Typer
from app.views.login import LoginView
from app.views.logout import LogoutView
from app.views.user import UserView
from app.views.client import ClientView
from app.views.contract import ContractView
from app.views.event import EventView
# from sentry_sdk import capture_exception

app = Typer()


@app.command(help="Login to the system.")
def login(email: str, password: str = None):
    # Sentry test
    # try:
    #     division_by_zero = 1 / 0
    # except ZeroDivisionError as e:
    #     capture_exception(e)
    view = LoginView()
    view.dispatch(email=email, password=password)


@app.command(help="Logout from the system.")
def logout():
    view = LogoutView()
    view.dispatch()


app.add_typer(UserView().app, name="user", help="User management commands.")

app.add_typer(ClientView().app, name="client", help="Client management commands.")

app.add_typer(ContractView().app, name="contract", help="Contract management commands.")

app.add_typer(EventView().app, name="event", help="Event management commands.")
