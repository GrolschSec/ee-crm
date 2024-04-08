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


def test_password_verification_valid():
    user = User(fullname="test", email="test@gmail.com", password="password")
    assert user.verify_password("password") is True


def test_password_verification_fail():
    user = User(fullname="test", email="test@gmail.com", password="password")
    assert user.verify_password("password123") is False


def test_create_valid_user():
    user = User(
        fullname="test", email="test@gmail.com", password="password", role="sales"
    )
    user = user.save()
    assert user.id is not None
    assert user.fullname == "test"
    assert user.email == "test@gmail.com"
    assert user.role == "sales"
    user.close()


def test_create_user_invalid_email():
    with pytest.raises(ValueError, match="Invalid email."):
        User(fullname="test", email="test", password="password", role="sales")


def test_create_user_invalid_role():
    with pytest.raises(ValueError, match="Role test not found."):
        User(fullname="test", email="test@gmail.com", password="password", role="test")
