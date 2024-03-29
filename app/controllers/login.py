from app.models import User
from os import path


class LoginController:
    TOKEN_PATH = path.join(path.expanduser("~"), ".ee_token")

    def __init__(self):
        self.token = None
        self.user_id = None
        self.email = None
        self.password = None

    def fetch_user_by_email(self):
        try:
            return User.get_instance(email=self.email)
        except Exception:
            return None

    def login(self, email: str, password: str):
        self.email = email
        self.password = password
        user = self.fetch_user_by_email()
        if user and user.verify_password(self.password):
            self.token = user.generate_jwt_token()
            return True
        return False

    def write_token_to_file(self):
        if not self.token:
            return False
        try:
            with open(self.TOKEN_PATH, "w") as f:
                f.write(self.token)
            return True
        except PermissionError:
            return False
