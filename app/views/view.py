from app.controllers.permission import isAuthenticated
from typer import echo
from typer import Typer


class View:
    permission_classes = []

    def dispatch(self, **kwargs):
        permissions = self.permission_classes

        if isinstance(permissions, dict):
            permissions = permissions.get(kwargs.get("request"), [])

        if isAuthenticated in permissions:
            auth = isAuthenticated()
            if not auth.has_permission():
                return echo("Permission Denied")
            kwargs["user"] = auth.user
        for permission in permissions:
            if not permission().has_permission(**kwargs):
                return echo("Permission Denied")
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
