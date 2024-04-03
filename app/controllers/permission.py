from app.models import User
from os import path
from typer import echo


class Permission:
    def has_permission(self, **kwargs):
        raise NotImplementedError
    
    def has_obj_permission(self, obj, **kwargs):
        raise NotImplementedError

class BasePermission(Permission):
    def has_permission(self, **kwargs):
        return True
    
    def has_obj_permission(self, obj, **kwargs):
        return True

class isAuthenticated(BasePermission):
    def has_permission(self, **kwargs):
        user = kwargs.get("user")
        if not user:
            return False
        return True


class isAdmin(isAuthenticated):
    def has_permission(self, **kwargs):
        if not super().has_permission(**kwargs):
            return False
        return kwargs.get("user").role.name == "admin"


class isManagementTeam(isAuthenticated):
    def has_permission(self, **kwargs):
        if not super().has_permission(**kwargs):
            return False
        return kwargs.get("user").role.name == "management"


class isSalesTeam(isAuthenticated):
    def has_permission(self, **kwargs):
        if not super().has_permission(**kwargs):
            return False
        return kwargs.get("user").role.name == "sales"


class isSupportTeam(isAuthenticated):
    def has_permission(self, **kwargs):
        if not super().has_permission(**kwargs):
            return False
        return kwargs.get("user").role.name == "support"


class AllowAny(BasePermission):
    def has_permission(self, **kwargs):
        return True

class isSalesReferent(isSalesTeam):
    def has_obj_permission(self, obj, **kwargs):
        return kwargs["user"].id == obj.sales_contact_id