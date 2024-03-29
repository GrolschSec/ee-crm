from app.models import User
from os import path
from typer import echo


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

    def read_token_from_file(self):
        try:
            with open(self.TOKEN_PATH, "r") as f:
                self.token = f.read()
        except PermissionError:
            self.token = None

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
        return kwargs.get("user").role.name == "admin"


class isManagementTeam(UserBasedPermission):
    def has_permission(self, **kwargs):
        if not super().has_permission(**kwargs):
            return False
        return kwargs.get("user").role.name == "management"


class isSalesTeam(UserBasedPermission):
    def has_permission(self, **kwargs):
        if not super().has_permission(**kwargs):
            return False
        return kwargs.get("user").role.name == "sales"


class isSupportTeam(UserBasedPermission):
    def has_permission(self, **kwargs):
        if not super().has_permission(**kwargs):
            return False
        return kwargs.get("user").role.name == "support"


class AllowAny(Permission):
    def has_permission(self, **kwargs):
        return True


class isAdminOrisManagementTeam(Permission):
    def has_permission(self, **kwargs):
        return isAdmin().has_permission(**kwargs) or isManagementTeam().has_permission(
            **kwargs
        )
