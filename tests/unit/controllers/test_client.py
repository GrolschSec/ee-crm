import pytest
from app.controllers.client import ClientController

def test_validate_fullname():
    controller = ClientController()
    assert controller.validate_fullname("John Doe") == True
    assert controller.validate_fullname("John") == False
