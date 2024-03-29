from app.views.view import CRUDView
from app.controllers.user import UserController
from typer import echo, prompt, Exit
from app.controllers.permission import (
    AllowAny,
    isAuthenticated,
    CreateIsAdminOrManagement,
)


class UserView(CRUDView):
    permission_classes = [AllowAny]

    def __init__(self) -> None:
        super().__init__()
        self.app.command("create")(self.handle_create)

    def handle_create(self, admin: bool = False):
        return super().handle_create(admin=admin)

    def create(self, admin: bool = False):
        if admin:
            UserAddAdminView().handle_create()
        else:
            UserAddUserView().handle_create()

    def user_creation(self):
        self.fullname = self.get_fullname()
        self.email = self.get_email()
        self.password = self.get_password()
        self.role = self.get_role()
        user = {
            "fullname": self.fullname,
            "email": self.email,
            "password": self.password,
            "role": self.role,
        }
        if UserController.create_user(user):
            echo("User created successfully.")

    def get_fullname(self):
        while True:
            fullname = prompt("Enter fullname")
            res = UserController.validate_fullname(fullname)
            if res[0]:
                return fullname
            echo(f"Error: {res[1]}")

    def get_email(self):
        while True:
            email = prompt("Enter email")
            if not UserController.validate_email(email):
                echo("Error: invalid email. Please try again.")
                continue
            if UserController.user_exist(email):
                echo("Error: user with that email already exists.")
                continue
            return email

    def get_password(self):
        while True:
            password = prompt("Enter password", hide_input=True)
            res = UserController.validate_password(password)
            if res[0]:
                return password
            echo(f"Error: {res[1]}")

    def get_role(self):
        if self.admin:
            return "admin"
        while True:
            echo("(1) - Management\n(2) - Sales\n(3) - Support")
            role_num = prompt("Select a role number")
            res = UserController.validate_role(role_num)
            if res[0]:
                return res[1]
            echo(f"Error: {res[1]}")


class UserAddAdminView(UserView):
    permission_classes = [AllowAny]

    def __init__(self) -> None:
        self.admin = True

    def create(self, **kwargs):
        if UserController.admin_exist():
            echo("Error: Admin already exists.")
            raise Exit(1)
        return self.user_creation()


class UserAddUserView(UserView):
    permission_classes = [isAuthenticated, CreateIsAdminOrManagement]

    def __init__(self) -> None:
        self.admin = False

    def create(self, **kwargs):
        return self.user_creation()
