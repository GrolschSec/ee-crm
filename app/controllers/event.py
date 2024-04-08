from app.controllers.controller import ModelController
from app.models.event import Event

class EventController(ModelController):

    model_class = Event
