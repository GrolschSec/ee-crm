from app.controllers.permission import isAuthenticated, AllowAny
from typer import echo

class View:
    permission_classes = []

    def dispatch(self, *args, **kwargs):
        if isAuthenticated in self.permission_classes:
            auth = isAuthenticated()
            if not auth.has_permission():
                return echo("Permission Denied")
            kwargs["user"] = auth.user
        for permission in self.permission_classes:
            if not permission().has_permission(**kwargs):
                return echo("Permission Denied")
        return self.handle(*args, **kwargs)

    def handle(self, *args, **kwargs):
        raise NotImplementedError
