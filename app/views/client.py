from app.controllers.client import ClientController
from app.views.view import CRUDView
from app.controllers.permission import (
    isSalesTeam,
    isSalesReferent,
    isAuthenticated,
)
from typer import echo, Exit
from tabulate import tabulate


class ClientView(CRUDView):
    controller_class = ClientController

    permission_classes = {
        "create": [isSalesTeam],
        "list": [isAuthenticated],
        "update": [isSalesReferent],
    }

    def __init__(self) -> None:
        super().__init__()
        self.app.command("create")(self.handle_create)
        self.app.command("list")(self.handle_list)
        self.app.command("update")(self.handle_update)

    def handle_create(
        self, fullname: str, email: str, phone: str, address: str, company_name: str
    ):
        return super().handle_create(
            fullname=fullname,
            email=email,
            phone=phone,
            address=address,
            company_name=company_name,
        )

    def create(self, **kwargs):
        kwargs["sales_contact_id"] = kwargs["user"].id
        self.controller.validate(**kwargs)
        if self.controller.is_valid():
            self.controller.save()
            echo("Client created successfully.")
        else:
            echo(f"Error: {self.controller.retrieve_error()}")
            raise Exit(1)

    def handle_list(self):
        return super().handle_list()

    def list(self, **kwargs):
        clients = self.controller.list()
        headers = ["ID", "Fullname", "Email", "Phone", "Address", "Company Name"]
        data = [
            [
                client.id,
                client.fullname,
                client.email,
                client.phone,
                client.address,
                client.company_name,
            ]
            for client in clients
        ]
        echo(tabulate(data, headers=headers, tablefmt="pretty"))

    def handle_update(
        self,
        pk: int,
        fullname: str = None,
        email: str = None,
        phone: str = None,
        address: str = None,
        company_name: str = None,
    ):
        return super().handle_update(
            pk=pk,
            fullname=fullname,
            email=email,
            phone=phone,
            address=address,
            company_name=company_name,
        )

    def update(self, **kwargs):
        echo(self.controller.update(**kwargs))
