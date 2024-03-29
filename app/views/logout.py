from app.views.view import View
from app.controllers.permission import AllowAny
from app.controllers.logout import LogoutController
from typer import echo, Exit


class LogoutView(View):
    permission_classes = [AllowAny]

    def __init__(self):
        self.logout_instance = LogoutController()

    def handle(self, *args, **kwargs):
        log_res = self.logout_instance.delete_token_file()
        if not log_res[0]:
            echo(f"Error: {log_res[1]}")
            raise Exit(1)
        echo("Logout successful.")
        raise Exit(0)
