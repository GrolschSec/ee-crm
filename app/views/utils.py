from app.controllers.user import UserController
from typer import echo, Exit, prompt, Option


# def check_authentication():
#     user = AuthController.verify_authentication()
#     if not user[0]:
#         echo("You are not authenticated.")
#         raise Exit(1)
#     return user[1]
