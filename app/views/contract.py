from app.controllers.contract import ContractController
from app.controllers.permission import isManagementTeam
from app.views.view import CRUDView
from typer import echo, Exit


class ContractView(CRUDView):

    controller_class = ContractController

    permission_classes = {
        "create": [isManagementTeam],
    }

    def __init__(self) -> None:
        super().__init__()
        self.app.command("create")(self.handle_create)

    def handle_create(self, client_id: int, amount_total: float, amount_due: float):
        return super().handle_create(
            client_id=client_id, amount_total=amount_total, amount_due=amount_due
        )

    def create(self, **kwargs):
        self.controller.validate(**kwargs)
        if self.controller.is_valid():
            self.controller.save()
            echo(f"Contract created successfully.")
        else:
            echo(f"Error: {self.controller.retrieve_error()}")
            raise Exit(1)
