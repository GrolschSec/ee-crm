from app.controllers.contract import ContractController
from app.controllers.permission import isManagementTeam, isAuthenticated, isManagementOrSalesReferentContract
from app.views.view import CRUDView
from typer import echo, Exit
from tabulate import tabulate


class ContractView(CRUDView):

    controller_class = ContractController

    permission_classes = {
        "create": [isManagementTeam],
        "list": [isAuthenticated],
        "update": [isManagementOrSalesReferentContract],
    }

    def __init__(self) -> None:
        super().__init__()
        self.app.command("create")(self.handle_create)
        self.app.command("list")(self.handle_list)
        self.app.command("update")(self.handle_update)

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
        
    def handle_list(self):
        return super().handle_list()
    
    def list(self, **kwargs):
        contracts = self.controller.list()
        headers = [
            "ID",
            "Client Name",
            "Client Company",
            "Total Amount",
            "Due Amount",
            "Creation date",
            "Status",
        ]
        data = [
            [
                contract.id,
                contract.client.fullname,
                contract.client.company_name,
                contract.amount_total,
                contract.amount_due,
                contract.creation_date,
                "Signed" if contract.is_signed else "Not signed"
            ]
            for contract in contracts
        ]
        echo(tabulate(data, headers=headers, tablefmt="pretty"))

    def handle_update(
        self,
        pk: int,
        amount_total: float = None,
        amount_due: float = None,
        is_signed: bool = None,
    ):
        return super().handle_update(
            pk=pk, amount_total=amount_total, amount_due=amount_due, is_signed=is_signed
        )
    
    def update(self, **kwargs):
        echo(self.controller.update(**kwargs))
    
    def handle_delete(self, pk: int):
        return super().handle_delete(pk=pk)
    
    def delete(self, **kwargs):
        echo(self.controller.delete(**kwargs))