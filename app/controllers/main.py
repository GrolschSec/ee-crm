from app.models import User
from os import path


class AuthController:
    TOKEN_PATH = path.join(path.expanduser("~"), ".ee_token")

    def try_get_user(**kwargs):
        try:
            return User.get_instance(**kwargs)
        except Exception as e:
            return None
    
    @classmethod
    def try_open_token_file(cls):
        try:
            with open(cls.TOKEN_PATH, "r") as f:
                cls.token = f.read()
        except PermissionError:
            cls.token = None

    @classmethod
    def login(cls, email: str = None, password: str = None):
        user = cls.try_get_user(email=email)
        if user is None:
            return {"valid": False}
        if user.verify_password(password):
            cls.token = user.generate_jwt_token()
            return {"valid": True}
        return {"valid": False}

    @classmethod
    def set_token(cls):
        try:
            with open(cls.TOKEN_PATH, "w") as f:
                f.write(cls.token)
            return True
        except PermissionError:
            return False

    @classmethod
    def check_path(cls):
        return path.exists(cls.TOKEN_PATH)

    @classmethod
    def is_authenticated(cls):
        if not cls.check_path():
            return False
        cls.try_open_token_file()
        if cls.token is None:
            return False
        cls.user_id = User.verify_jwt_token(cls.token)
        if cls.user_id is None:
            return False
        if cls.try_get_user(id=cls.user_id) is None:
            return False
        return True
