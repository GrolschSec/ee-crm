import pytest
from app.controllers.user import UserController

def test_validate_fullname():
    controller = UserController()
    assert controller.validate_fullname("John Doe") == True
    assert controller.validate_fullname("John") == False

def test_validate_password():
    controller = UserController()
    assert controller.validate_password("JohnDoe123!") == True
    assert controller.validate_password("JohnDoe") == False

def test_validate_role():
    controller = UserController()
    controller.values = {}
    assert controller.validate_role("management") == True
    assert controller.validate_role("admin") == False
