import pytest
from app.models import Contract
from datetime import date

def test_contract_attributes(client):
    client_id = client.id
    client.close()
    contract = Contract(
        client_id=client_id,
        amount_total=1000.00,
        amount_due=500.00,
    )
    contract.save()
    assert contract.client_id == client_id
    assert contract.amount_total == 1000.00
    assert contract.amount_due == 500.00
    assert isinstance(contract.creation_date, date)
