from app.models.role import Role


class RoleController:
    @staticmethod
    def check_and_create_roles():
        roles_to_check = ["management", "sales", "support", "admin", "anonymous"]
        for role_name in roles_to_check:
            role = Role.get_instance(name=role_name)
            if not role:
                new_role = Role(name=role_name)
                new_role.save()
