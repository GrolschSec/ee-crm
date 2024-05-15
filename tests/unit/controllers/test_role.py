import pytest
from app.controllers.role import RoleController
from app.models.role import Role

def test_check_and_create_roles():
    controller = RoleController()
    controller.check_and_create_roles()
    roles = Role.all()[0]
    assert len(roles) == 5
    assert roles[0].name == 'management'
    assert roles[2].name == 'sales'
    assert roles[1].name == 'support'
    assert roles[3].name == 'admin'
    assert roles[4].name == 'anonymous'

