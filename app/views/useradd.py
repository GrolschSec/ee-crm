from app.views.view import View
from app.controllers.permission import (
    isAuthenticated,
    AllowAny,
    isAdminOrisManagementTeam
)
from app.controllers.user import UserController
from typer import prompt, echo, Exit


class UserAddView(View):

    def __init__(self, admin: bool = False):
        self.admin = admin

    def handle(self, *args, **kwargs):
        self.fullname = self.get_fullname()
        self.email = self.get_email()
        self.password = self.get_password()
        self.role = self.get_role()

        user = {"fullname": self.fullname, "email": self.email, "password": self.password, "role": self.role}
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

class UserAddAdminView(View):
    permission_classes = [AllowAny]

    def handle(self, *args, **kwargs):
        if UserController.admin_exist():
            echo("Admin user already exists.")
            raise Exit(1)
        view = UserAddView(admin=True)
        view.dispatch()


class UserAddUserView(View):
    permission_classes = [isAuthenticated, isAdminOrisManagementTeam]

    def handle(self, *args, **kwargs):
        view = UserAddView()
        view.dispatch()
