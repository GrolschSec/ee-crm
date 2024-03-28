from app.controllers.authentication import AuthController
from app.controllers.user import UserController
from typer import echo, Exit, prompt, Option


def check_authentication():
    user = AuthController.verify_authentication()
    if not user[0]:
        echo("You are not authenticated.")
        raise Exit(1)
    return user[1]


def user_creation(admin: bool = False):
    fullname = None
    email = None
    password = None
    role = None
    role_num = None
    while True:
        if fullname is None:
            fullname = prompt("Enter fullname")
        fullname_res = UserController.validate_fullname(fullname)
        if not fullname_res[0]:
            echo(f"Error: {fullname_res[1]}")
            fullname = None
            continue
        if email is None:
            email = prompt("Enter email")
        email_res = UserController.validate_email(email)
        if not email_res:
            echo("Error: invalid email. Please try again.")
            email = None
            continue
        if UserController.user_exist(email):
            echo("Error: user with that email already exists.")
            email = None
            continue
        if password is None:
            password = prompt("Enter password", hide_input=True)
        password_res = UserController.validate_password(password)
        if not password_res[0]:
            echo(f"Error: {password_res[1]}")
            password = None
            continue
        if role is None and not admin:
            echo("(1) - Management\n(2) - Sales\n(3) - Support")
            role_num = prompt("Select a role number")
        role_res = UserController.validate_role(role_num)
        if not role_res[0] and not admin:
            echo(f"Error: {role_res[1]}")
            role = None
            continue
        else:
            role = role_res[1]
        break
    if admin:
        role = "admin"
    user = {"fullname": fullname, "email": email, "password": password, "role": role}
    if UserController.create_user(user):
        echo("User created successfully.")
