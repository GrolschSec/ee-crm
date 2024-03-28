from models import User


class Permission:

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
