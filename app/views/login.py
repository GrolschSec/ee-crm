from app.views.view import View
from app.controllers.permission import AllowAny
from app.controllers.login import LoginController
from typer import echo, prompt, Exit


class LoginView(View):
    permission_classes = [AllowAny]

    def __init__(self):
        self.email = None
        self.password = None
        self.login_instance = LoginController()

    def handle(self, **kwargs):
        self.get_password(**kwargs)
        self.authenticate(**kwargs)

    def get_password(self, **kwargs):
        password = kwargs.get("password")
        if password is None:
            password = prompt("Enter your password", hide_input=True)
        self.password = password

    def authenticate(self, **kwargs):
        email = kwargs.get("email")
        login = self.login_instance.login(email, self.password)
        if login:
            if not self.login_instance.write_token_to_file():
                echo("Error: failed to save token.")
                raise Exit(1)
            echo("Login successful.")
        else:
            echo("Invalid credentials, please try again.")
            raise Exit(1)
