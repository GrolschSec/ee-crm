from app.models import User
from os import path


class Permission:
    def has_permission(self, **kwargs):
        raise NotImplementedError


class isAuthenticated(Permission):
    TOKEN_PATH = path.join(path.expanduser("~"), ".ee_token")

    def __init__(self):
        self.token = None
        self.user_id = None
        self.user = None

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

    def has_permission(self, **kwargs):
        if not self.is_token_file_present():
            return False
        self.read_token_from_file()
        if not self.token:
            return False
        self.user_id = User.verify_jwt_token(self.token)
        self.user = User.get_instance(id=self.user_id)
        return self.user is not None


class UserBasedPermission(Permission):
    def has_permission(self, **kwargs):
        user = kwargs.get("user")
        if not user:
            return False
        return True


class isAdmin(UserBasedPermission):
    def has_permission(self, **kwargs):
        if not super().has_permission(**kwargs):
            return False
        return kwargs.get("user").role == "admin"


class isManagementTeam(UserBasedPermission):
    def has_permission(self, **kwargs):
        if not super().has_permission(**kwargs):
            return False
        return kwargs.get("user").role == "management"


class isSalesTeam(UserBasedPermission):
    def has_permission(self, **kwargs):
        if not super().has_permission(**kwargs):
            return False
        return kwargs.get("user").role == "sales"


class isSupportTeam(UserBasedPermission):
    def has_permission(self, **kwargs):
        if not super().has_permission(**kwargs):
            return False
        return kwargs.get("user").role == "support"


class AllowAny(Permission):
    def has_permission(self, **kwargs):
        return True
