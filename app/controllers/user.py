from app.models import User, Role
from email_validator import validate_email, EmailNotValidError


class UserController:

    @staticmethod
    def admin_exist():
        return User.get_first_by_role(name="admin") is not None

    @staticmethod
    def user_exist(**kwargs):
        if User.get_instance(**kwargs) is not None:
            return True
        return False

    @staticmethod
    def validate_email(email):
        try:
            validate_email(email)
            return True
        except EmailNotValidError as e:
            return False

    @staticmethod
    def validate_fullname(fullname):
        if (len(fullname) < 6) or (len(fullname) > 50):
            return [False, "Fullname must be between 6 and 50 characters."]
        if not fullname.replace(" ", "").isalpha():
            return [False, "Fullname must contain only alphabets."]
        return [True, None]

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            return [False, "Password must be at least 8 characters."]
        if not any(char.isdigit() for char in password):
            return [False, "Password must contain at least one digit."]
        if not any(char.isupper() for char in password):
            return [False, "Password must contain at least one uppercase letter."]
        if not any(char.islower() for char in password):
            return [False, "Password must contain at least one lowercase letter."]
        if not any(char in "!@#$%^&*()-+" for char in password):
            return [False, "Password must contain at least one special character."]
        return [True, None]

    @staticmethod
    def validate_role(role):
        if role == "1":
            return [True, "management"]
        elif role == "2":
            return [True, "sales"]
        elif role == "3":
            return [True, "support"]
        return [False, "Invalid role number."]

    @staticmethod
    def create_user(user):
        role_id = Role.get_instance(name=user["role"]).id
        user = User(
            fullname=user["fullname"],
            email=user["email"],
            password=user["password"],
            role_id=role_id,
        )
        user.save()
        return True
    
    @staticmethod
    def update_user(**kwargs):
        updated = False
        user = User.get_instance(id=kwargs.get("user_id"))

        if kwargs.get("fullname"):
            user.fullname = kwargs.get("fullname")
            updated = True
        if kwargs.get("email"):
            user.email = kwargs.get("email")
            updated = True
        if kwargs.get("role"):
            user.role_id = Role.get_instance(name=kwargs.get("role")).id
            updated = True
        if kwargs.get("password"):
            user.password = kwargs.get("password")
            updated = True
        if updated:
            user.save()
        return updated
    
    @staticmethod
    def anonymize(**kwargs):
        user = User.get_instance(id=kwargs.get("user_id"))
        user.fullname = "Anonymous"
        user.email = "anonymous@anonymous.com"
        user._password = "Anonymous"
        user.role_id = Role.get_instance(name="anonymous").id
        user.save()

    @staticmethod
    def get_user(**kwargs):
        return User.get_instance(**kwargs)
