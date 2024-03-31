from app.views.view import CRUDView
from app.controllers.user import UserController
from typer import echo, prompt, Exit, Option
from tabulate import tabulate
from app.controllers.permission import (
    AllowAny,
    isAuthenticated,
    CreateIsAdminOrManagement,
    isAdminOrisManagementTeam,
)


class UserView(CRUDView):
    permission_classes = {
        "create": [AllowAny],
        "list": [isAuthenticated, isAdminOrisManagementTeam],
        "update": [isAuthenticated, isAdminOrisManagementTeam],
        "delete": [isAuthenticated, isAdminOrisManagementTeam],
    }

    def __init__(self) -> None:
        super().__init__()
        self.app.command("create")(self.handle_create)
        self.app.command("list")(self.handle_list)
        self.app.command("update")(self.handle_update)
        self.app.command("delete")(self.handle_delete)

    def handle_create(self, admin: bool = False):
        return super().handle_create(admin=admin)

    def create(self, admin: bool = False):
        if admin:
            UserAddAdminView().handle_create()
        else:
            UserAddUserView().handle_create()

    def handle_list(self):
        return super().handle_list()

    def list(self, **kwargs):
        users = UserController.get_all_users()
        table = [(user.id, user.fullname, user.email, user.role.name) for user in users]
        echo(
            tabulate(
                table, headers=["ID", "Fullname", "Email", "Role"], tablefmt="pretty"
            )
        )

    def handle_update(
        self,
        user_id: int,
        fullname: str = None,
        email: str = None,
        role: str = None,
        password: str = None,
    ):
        return super().handle_update(
            user_id=user_id,
            fullname=fullname,
            email=email,
            role=role,
            password=password,
        )

    def update(self, **kwargs):
        self.user_exist(**kwargs)
        if (
            kwargs.get("fullname")
            and not UserController.validate_fullname(kwargs.get("fullname"))[0]
        ):
            echo("Error: Invalid fullname.")
            raise Exit(1)
        if kwargs.get("email") and not UserController.validate_email(
            kwargs.get("email")
        ):
            echo("Error: Invalid email.")
            raise Exit(1)
        if (
            kwargs.get("role")
            and not UserController.validate_role(kwargs.get("role"))[0]
        ):
            echo("Error: Invalid role. Roles: management, sales, support.")
            raise Exit(1)
        if (
            kwargs.get("password")
            and not UserController.validate_password(kwargs.get("password"))[0]
        ):
            echo(
                f"Error: {UserController.validate_password(kwargs.get('password'))[1]}"
            )
            raise Exit(1)
        if UserController.update_user(**kwargs):
            echo("User updated successfully.")
        else:
            echo("You need to specify at least one field to update.")

    def handle_delete(self, user_id: int):
        return super().handle_delete(user_id=user_id)

    def delete(self, **kwargs):
        self.user_exist(**kwargs)
        user = UserController.get_user(id=kwargs.get("user_id"))
        answer = prompt(f"Are you sure you want to delete user {user.fullname} ? (y/n)")
        if answer.lower() == "y":
            UserController.anonymize(**kwargs)
            echo("User deleted successfully.")
        else:
            echo("Operation cancelled.")

    def user_exist(self, **kwargs):
        if not UserController.user_exist(id=kwargs.get("user_id")):
            echo("Error: User not found.")
            raise Exit(1)

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
            if UserController.user_exist(email=email):
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
