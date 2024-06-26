from app.models import User
from os import path
from app.controllers.controller import ModelController
from uuid import uuid4


class UserController(ModelController):
    model_class = User

    TOKEN_PATH = token_path = path.join(path.expanduser("~"), ".ee_token")

    def validate_fullname(self, fullname):
        self.init_errors_field("fullname")
        if (len(fullname) < 6) or (len(fullname) > 50):
            self.errors["fullname"] = "Fullname must be between 6 and 50 characters."
            return False
        if not fullname.replace(" ", "").isalpha():
            self.errors["fullname"] = "Fullname must contain only alphabets."
            return False
        return True

    def validate_password(self, password):
        self.init_errors_field("password")
        if len(password) < 8:
            self.errors["password"] = "Password must be at least 8 characters."
            return False
        if not any(char.isdigit() for char in password):
            self.errors["password"] = "Password must contain at least one digit."
            return False
        if not any(char.isupper() for char in password):
            self.errors["password"] = (
                "Password must contain at least one uppercase letter."
            )
            return False
        if not any(char.islower() for char in password):
            self.errors["password"] = (
                "Password must contain at least one lowercase letter."
            )
            return False
        if not any(char in "!@#$%^&*()-+" for char in password):
            self.errors["password"] = (
                "Password must contain at least one special character."
            )
            return False
        return True

    def validate_role(self, role: str):
        self.init_errors_field("role")
        role = role.lower()
        if role != "management" and role != "sales" and role != "support":
            self.errors["role"] = "Invalid role."
            return False
        self.values["role"] = role
        return True

    @classmethod
    def is_token_file_present(cls):
        return path.exists(cls.TOKEN_PATH)

    @classmethod
    def read_token_from_file(cls):
        try:
            with open(cls.TOKEN_PATH, "r") as f:
                cls.token = f.read()
        except PermissionError:
            cls.token = None

    @classmethod
    def authenticate(cls):
        if not cls.is_token_file_present():
            return None
        cls.read_token_from_file()
        if not cls.token:
            return None
        cls.user_id = User.verify_jwt_token(cls.token)
        cls.user = User.get_instance(id=cls.user_id)
        return cls.user

    def delete(self, **kwargs):
        obj = kwargs.get("obj")
        if obj is None:
            return "No object provided for delete."
        obj.fullname = "Unknown"
        obj.email = f"{uuid4()}@unkown.com"
        obj.password = str(uuid4())
        obj.role = "anonymous"
        obj.is_active = False
        obj.save()
        obj.close()
        return "User deleted successfully."
