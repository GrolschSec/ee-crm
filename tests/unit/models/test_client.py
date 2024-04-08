import pytest
from app.models import Base, Client
from datetime import date, datetime


def test_client_attributes():
    client = Client(
        fullname="Test Client",
        email="test@gmail.com",
        phone="+33695454332",
        address="123 Test St",
        company_name="Test Company",
        sales_contact_id=1,
    )
    client.save()

    assert client.fullname == "Test Client"
    assert client.email == "test@gmail.com"
    assert client.phone == "+33695454332"
    assert client.address == "123 Test St"
    assert client.company_name == "Test Company"
    assert client.sales_contact_id == 1
    assert isinstance(client.creation_date, date)
    assert isinstance(client.last_update, datetime)
    client.close()


def test_client_invalid_phone_number():
    with pytest.raises(ValueError, match="Invalid phone number."):
        client = Client(
            fullname="Test Client",
            email="test@gmail.com",
            phone="+3369545",
            address="123 Test St",
            company_name="Test Company",
            sales_contact_id=1,
        )


def test_client_invalid_email():
    with pytest.raises(ValueError, match="Invalid email."):
        client = Client(
            fullname="Test Client",
            email="test@s.com",
            phone="+33695452233",
            address="123 Test St",
            company_name="Test Company",
            sales_contact_id=1,
        )
