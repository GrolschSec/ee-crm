from app.controllers.controller import ModelController
from app.models import Event, Contract
from datetime import datetime


class EventController(ModelController):

    model_class = Event

    def validate_contract_id(self, contract_id):
        is_valid = False
        self.init_errors_field("contract_id")
        contract = Contract().get_instance(id=contract_id)
        if contract is None:
            self.errors["contract_id"] = "Contract not found."
            return is_valid
        if contract.is_signed:
            event = self.model_class().get_instance(contract_id=contract_id)
            if event is not None:
                self.errors["contract_id"] = "Event already exists for this contract."
                event.close()
                return False
            is_valid = True
        else:
            self.errors["contract_id"] = "Contract is not signed."
        contract.close()
        return is_valid

    def validate_time(self, date_str):
        try:
            date = datetime.strptime(date_str, "%d/%m/%Y")
            if date < datetime.now():
                return None
            return date.strftime("%Y-%m-%d")
        except ValueError:
            return None

    def validate_start_date(self, start_date):
        self.init_errors_field("start_date")
        if not start_date:
            self.errors["start_date"] = "Start date is required."
            return
        start_date = self.validate_time(start_date)
        if not start_date:
            self.errors["start_date"] = "Invalid start date."
        else:
            self.values["start_date"] = start_date

    def validate_end_date(self, end_date):
        self.init_errors_field("end_date")
        if not end_date:
            self.errors["end_date"] = "End date is required."
            return
        end_date = self.validate_time(end_date)
        if not end_date:
            self.errors["end_date"] = "Invalid end date."
        else:
            self.values["end_date"] = end_date
