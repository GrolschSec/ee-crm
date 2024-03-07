import pytest
from app.models import User


def test_user_attributes():
    user = User(fullname="test", email="test@gmail.com", password="password")
    assert user.fullname == "test"
    assert user.email == "test@gmail.com"
    assert user.password != "password"


def test_password_hashing():
    user = User(fullname="test", email="test@gmail.com", password="password")
    assert user._password != "password"


def test_password_verification():
    user = User(fullname="test", email="test@gmail.com", password="password")
    assert user.verify_password("password") is True


def test_user_relationships(role_management, session):
    user = User(
        fullname="test",
        email="test@gmail.com",
        password="password",
        role_id=role_management.id,
    )
    session.add(user)
    session.commit()
    assert user.role_id == role_management.id
    assert user.role.name == "management"
