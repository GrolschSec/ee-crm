import pytest
from app.models import Event
from datetime import datetime

def test_event_attributes(contract, support_user):
    contract_id = contract.id
    contract.close()
    support_user_id = support_user.id
    support_user.close()
    start_date=datetime.strptime("2021-05-01", "%Y-%m-%d")
    end_date=datetime.strptime("2021-06-01", "%Y-%m-%d")
    event = Event(
        start_date=start_date,
        end_date=end_date,
        location="Test Location",
        attendees_count=10,
        notes="Test Notes",
        contract_id=contract_id,
        support_contact_id=support_user_id,
    )
    event.save()
    assert event.contract_id == contract_id
    assert event.support_contact_id == support_user.id
    assert event.start_date == start_date
    assert event.end_date == end_date
    assert event.location == "Test Location"
    assert event.attendees_count == 10
    assert event.notes == "Test Notes"
    assert event.contract_id == contract_id
    assert event.support_contact_id == support_user_id
    event.close()