from app.views.view import CRUDView
from app.controllers.event import EventController
from app.controllers.permission import isAuthenticated, isSalesReferentEvent, isSalesReferentEventOrManagementTeam
from typer import echo, Exit
from tabulate import tabulate


class EventView(CRUDView):
    controller_class = EventController

    permission_classes = {
        "create": [isSalesReferentEvent],
        "list": [isAuthenticated],
        "update": [isSalesReferentEventOrManagementTeam],
    }

    def __init__(self) -> None:
        super().__init__()
        self.app.command("create")(self.handle_create)
        self.app.command("list")(self.handle_list)
        self.app.command("update")(self.handle_update)

    def handle_create(
        self,
        start_date: str,
        end_date: str,
        location: str,
        attendees_count: int,
        notes: str,
        contract_id: int,
    ):
        return super().handle_create(
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendees_count=attendees_count,
            notes=notes,
            contract_id=contract_id,
        )

    def create(self, **kwargs):
        self.controller.validate(**kwargs)
        if self.controller.is_valid():
            self.controller.save()
            echo(f"Event created successfully.")
        else:
            echo(f"Error: {self.controller.retrieve_error()}")
            raise Exit(1)

    def handle_list(self):
        return super().handle_list()

    def list(self, **kwargs):
        events = self.controller.list()
        headers = [
            "ID",
            "Start Date",
            "End Date",
            "Location",
            "Attendees Count",
            "Notes",
            "Contract ID",
            "Support Contact",
        ]
        data = [
            [
                event.id,
                event.start_date,
                event.end_date,
                event.location,
                event.attendees_count,
                event.notes,
                event.contract_id,
                (
                    "Not assigned"
                    if event.support_contact_id is None
                    else event.support_contact.fullname
                ),
            ]
            for event in events
        ]
        echo(tabulate(data, headers=headers, tablefmt="pretty"))

    def handle_update(
        self,
        pk: int,
        start_date: str = None,
        end_date: str = None,
        location: str = None,
        attendees_count: int = None,
        notes: str = None,
        support_contact_id: int = None,
    ):
        return super().handle_update(
            pk=pk,
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendees_count=attendees_count,
            notes=notes,
            support_contact_id=support_contact_id,
        )

    def update(self, **kwargs):
        echo(self.controller.update(**kwargs))
        
