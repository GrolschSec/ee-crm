from app.views.view import CRUDView
from app.controllers.permission import isAuthenticated, isAdminOrSalesTeam
from typer import echo


class ClientView(CRUDView):
    permission_classes = {"create": [isAuthenticated, isAdminOrSalesTeam]}

    def __init__(self) -> None:
        super().__init__()
        self.app.command("create")(self.handle_create)

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
        pass
