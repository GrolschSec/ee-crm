from app.models import User
from os import path


class AuthController:
    TOKEN_PATH = path.join(path.expanduser("~"), ".ee_token")

    def __init__(self):
        self.token = None
        self.user_id = None

    @staticmethod
    def fetch_user_by_email(email: str):
        try:
            return User.get_instance(email=email)
        except Exception:
            return None

    @classmethod
    def read_token_from_file(cls):
        try:
            with open(cls.TOKEN_PATH, "r") as f:
                cls.token = f.read()
        except PermissionError:
            cls.token = None

    @classmethod
    def login(cls, email: str, password: str):
        user = cls.fetch_user_by_email(email)
        if user and user.verify_password(password):
            cls.token = user.generate_jwt_token()
            return {"valid": True, "user": user}
        return {"valid": False, "user": None}

    @classmethod
    def write_token_to_file(cls):
        if not cls.token:
            return False
        try:
            with open(cls.TOKEN_PATH, "w") as f:
                f.write(cls.token)
            return True
        except PermissionError:
            return False

    @classmethod
    def is_token_file_present(cls):
        return path.exists(cls.TOKEN_PATH)

    @classmethod
    def verify_authentication(cls):
        if not cls.is_token_file_present():
            return [False, None]
        cls.read_token_from_file()
        if not cls.token:
            return [False, None]
        cls.user_id = User.verify_jwt_token(cls.token)
        user = User.get_instance(id=cls.user_id)
        return [user is not None, user]
