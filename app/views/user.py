from app.views.view import CRUDView
from app.controllers.user import UserController
from typer import echo, prompt, Exit
from tabulate import tabulate
from app.controllers.permission import (
    AllowAny,
    isAuthenticated,
    isManagementTeam,
)


class UserView(CRUDView):
    controller_class = UserController

    permission_classes = {
        "create": [AllowAny],
    }

    def __init__(self) -> None:
        super().__init__()
        self.app.command("create")(self.handle_create)

    def handle_create(
        self,
        fullname: str,
        email: str,
        role: str,
        password: str = None,
        admin: bool = False,
    ):
        kwargs = {
            "fullname": fullname,
            "email": email,
            "role": role,
            "password": password,
            "admin": admin,
            "request": "create",
        }
        if admin:
            UserAddAdminView().handle_create(**kwargs)
        else:
            UserAddUserView().handle_create(**kwargs)

    def create(self, **kwargs):
        if "admin" in kwargs:
            kwargs.pop("admin")
        if not kwargs.get("password"):
            kwargs["password"] = self.get_password()
        self.controller.validate(**kwargs)
        if self.controller.is_valid():
            self.controller.save()
            echo("User created successfully.")
        else:
            echo("Error: Invalid data.")
            echo(self.controller.errors)

    def get_password(self):
        while True:
            password = prompt("Enter password", hide_input=True)
            res = self.controller.validate_password(password)
            if not res:
                echo(f"Error: {self.controller.errors['password']}")
                continue
            return password


class UserAddAdminView(UserView):
    permission_classes = [AllowAny]

    def handle_create(self, **kwargs):
        self.dispatch(**kwargs)

    def create(self, **kwargs):
        if self.controller.get_object(is_admin=True):
            echo("Error: Admin user already exists.")
            raise Exit(1)
        kwargs["is_admin"] = True
        kwargs["role"] = "admin"
        super().create(**kwargs)


class UserAddUserView(UserView):
    permission_classes = [isAuthenticated, isManagementTeam]

    def handle_create(self, **kwargs):
        self.dispatch(**kwargs)
