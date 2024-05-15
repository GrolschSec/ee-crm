import pytest
from app.controllers.event import EventController


def test_validate_contract_id():
    controller = EventController()
    assert controller.validate_contract_id(1) is False

