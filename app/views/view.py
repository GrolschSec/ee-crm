from app.controllers.permission import isAdmin
from app.controllers.user import UserController
from typer import Typer, Exit, echo


class View:
    permission_classes = []

    controller_class = None

    def get_object(self, pk):
        if self.controller_class is None:
            return None
        return self.controller_class.get_object(id=pk)

    def get_permission(self, **kwargs):
        permissions = self.permission_classes

        if isinstance(permissions, dict):
            permissions = permissions.get(kwargs.get("request"), [])

        return permissions

    def check_permissions(self, **kwargs):
        for permission in self.get_permission(**kwargs):
            if not permission().has_permission(**kwargs):
                return False
        return True

    def check_obj_permissions(self, **kwargs):
        for permission in self.get_permission(**kwargs):
            if kwargs.get("obj") and not permission().has_obj_permission(**kwargs):
                return False
        return True

    def perform_authentication(self, kwargs):
        kwargs["user"] = UserController.authenticate()

    def dispatch(self, **kwargs):
        self.perform_authentication(kwargs)

        if "pk" in kwargs:
            kwargs["obj"] = self.get_object(kwargs["pk"])

        if not self.check_permissions(**kwargs) or not self.check_obj_permissions(
            **kwargs
        ):
            echo("Permission denied.")
            raise Exit(1)

        return self.handle(**kwargs)

    def handle(self, **kwargs):
        raise NotImplementedError


class CRUDView(View):
    def __init__(self) -> None:
        self.app = Typer()

    def handle_create(self, **kwargs):
        self.dispatch(request="create", **kwargs)

    def handle_read(self, **kwargs):
        self.dispatch(request="read", **kwargs)

    def handle_list(self, **kwargs):
        self.dispatch(request="list", **kwargs)

    def handle_update(self, **kwargs):
        self.dispatch(request="update", **kwargs)

    def handle_delete(self, **kwargs):
        self.dispatch(request="delete", **kwargs)

    def create(self, **kwargs):
        raise NotImplementedError

    def read(self, **kwargs):
        raise NotImplementedError

    def list(self, **kwargs):
        raise NotImplementedError

    def update(self, **kwargs):
        raise NotImplementedError

    def delete(self, **kwargs):
        raise NotImplementedError

    def handle(self, **kwargs):
        request = kwargs.get("request")
        kwargs.pop("request")
        if request == "create":
            return self.create(**kwargs)
        elif request == "read":
            return self.read(**kwargs)
        elif request == "list":
            return self.list(**kwargs)
        elif request == "update":
            return self.update(**kwargs)
        elif request == "delete":
            return self.delete(**kwargs)
        else:
            raise NotImplementedError
