from app.controllers.controller import ModelController
from app.models.contract import Contract
from app.models.client import Client


class ContractController(ModelController):

    model_class = Contract

    def __init__(self):
        super().__init__()
        self.amount_due = None
        self.amount_total = None

    def validate_client_id(self, client_id):
        self.init_errors_field("client_id")
        if not client_id:
            self.errors["client_id"] = "Client ID is required."
        client = Client().get_instance(id=client_id)
        if client is None:
            self.errors["client_id"] = "Client not found."
            return False
        else:
            client.close()
        return True
    
    def validate_amount_total(self, amount_total):
        self.init_errors_field("amount_total")
        if not amount_total:
            self.errors["amount_total"] = "Total amount is required."
            return False
        if self.amount_due is None:
            self.amount_total = amount_total
        else:
            if amount_total < self.amount_due:
                self.errors["amount_total"] = "Total amount must be greater than due amount."
                return False
        return True

    def validate_amount_due(self, amount_due):
        self.init_errors_field("amount_due")
        if not amount_due:
            self.errors["amount_due"] = "Due amount is required."
            return False
        if self.amount_total is None:
            self.amount_due = amount_due
        else:
            if amount_due > self.amount_total:
                self.errors["amount_due"] = "Total amount must be greater than due amount."
                return False
        return True

    def delete(self, **kwargs):
        raise NotImplementedError