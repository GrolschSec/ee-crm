import pytest
from app.controllers.contract import ContractController

def test_validate_client_id():
    controller = ContractController()
    assert controller.validate_client_id(0) == False
    assert controller.validate_client_id(0) == False
    assert controller.validate_client_id(None) == False

def test_validate_amount_total():
    controller = ContractController()
    assert controller.validate_amount_total(0) == False
    assert controller.validate_amount_total(0) == False
    assert controller.validate_amount_total(None) == False
    assert controller.validate_amount_total(100) == True

def test_validate_amount_due():
    controller = ContractController()
    assert controller.validate_amount_due(0) == False
    assert controller.validate_amount_due(0) == False
    assert controller.validate_amount_due(None) == False
    assert controller.validate_amount_due(100) == True
    