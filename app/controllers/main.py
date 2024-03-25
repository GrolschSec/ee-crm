from app.models import User
from os import path
from email_validator import validate_email, EmailNotValidError


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
            return [False, None]
        cls.try_open_token_file()
        if cls.token is None:
            return [False, None]
        cls.user_id = User.verify_jwt_token(cls.token)
        if cls.user_id is None:
            return [False, None]
        user = cls.try_get_user(id=cls.user_id)
        if user is None:
            return [False, None]
        return [True, user]

class PermissionsController:

    @staticmethod
    def is_admin(user: User):
        return user.role.name == "admin"

    @staticmethod
    def is_sales_user(user: User):
        return user.role.name == "sales"

    @staticmethod
    def is_support_user(user: User):
        return user.role.name == "support"

    @staticmethod
    def is_management_user(user: User):
        return user.role.name == "management"
    
class UserController:

    @classmethod
    def is_email_valid(email: str):
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    
    