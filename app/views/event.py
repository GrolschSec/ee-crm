from app.views.view import CRUDView
from app.controllers.event import EventController
from app.controllers.permission import isAuthenticated


class EventView(CRUDView):
    controller_class = EventController

    permission_classes = {
        "list": [isAuthenticated],
    }
