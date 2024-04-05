from app.models import Client
from app.controllers.controller import ModelController


class ClientController(ModelController):
    model_class = Client

    def validate_fullname(self, fullname):
        self.init_errors_field("fullname")
        if (len(fullname) < 6) or (len(fullname) > 50):
            self.errors["fullname"] = "Fullname must be between 6 and 50 characters."
            return False
        if not fullname.replace(" ", "").isalpha():
            self.errors["fullname"] = "Fullname must contain only alphabets."
            return False
        return True
