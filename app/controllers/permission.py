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
        return kwargs.get("user").role == "admin"


class isManagementTeam(isAuthenticated):
    def has_permission(self, **kwargs):
        if not super().has_permission(**kwargs):
            return False
        return kwargs.get("user").role == "management"


class isSalesTeam(isAuthenticated):
    def has_permission(self, **kwargs):
        if not super().has_permission(**kwargs):
            return False
        return kwargs.get("user").role == "sales"


class isSupportTeam(isAuthenticated):
    def has_permission(self, **kwargs):
        if not super().has_permission(**kwargs):
            return False
        return kwargs.get("user").role == "support"


class AllowAny(BasePermission):
    def has_permission(self, **kwargs):
        return True


class isSalesReferent(isSalesTeam):
    def has_obj_permission(self, obj, **kwargs):
        return kwargs["user"].id == obj.sales_contact_id


class isAdminSpecialObject(isAuthenticated):
    def has_obj_permission(self, obj, **kwargs):
        if obj.is_admin:
            return kwargs.get("user").role == "admin"
        return True


class isSalesOrManagement(isAuthenticated):
    def has_permission(self, **kwargs):
        return isSalesTeam().has_permission(
            **kwargs
        ) or isManagementTeam().has_permission(**kwargs)


class isManagementOrSalesReferentContract(isAuthenticated):

    def has_obj_permission(self, obj, **kwargs):
        if isManagementTeam().has_permission(**kwargs):
            return True
        return (
            isSalesTeam().has_permission(**kwargs)
            and obj.client.sales_contact_id == kwargs["user"].id
        )


class isSalesReferentEvent(isAuthenticated):

    def has_obj_permission(self, obj, **kwargs):
        return isSalesTeam and kwargs["user"].id == obj.contract.client.sales_contact_id


class isSalesReferentEventOrManagementTeam(isAuthenticated):

    def has_obj_permission(self, obj, **kwargs):
        return isManagementTeam().has_permission(
            **kwargs
        ) or isSalesReferentEvent().has_obj_permission(obj, **kwargs)
