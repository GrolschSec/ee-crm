from app.controllers.permission import isAuthenticated, AllowAny


class View:
    permission_classes = []

    def dispatch(self, *args, **kwargs):
        if isAuthenticated in self.permission_classes:
            auth = isAuthenticated()
            if not auth.has_permission():
                return "Permission Denied"
            kwargs["user"] = auth.user
        for permission in self.permission_classes:
            if not permission().has_permission(**kwargs):
                return "Permission Denied"
        return self.handle(*args, **kwargs)

    def handle(self, *args, **kwargs):
        raise NotImplementedError
