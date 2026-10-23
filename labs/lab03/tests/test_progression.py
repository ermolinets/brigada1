import pytest
from datetime import date, datetime, timezone
from decimal import Decimal
from app import api
from app.support.errors import DomainError


def code(expected, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == expected

from app.domain.customer import Customer
from app.support.types import CustomerContext

def test_progression_availability_does_not_cache_state():
    service = api.create()
    item = Customer("C", "Alice", "STANDARD")

    service.register(item)
    first = service.check("C", CustomerContext())
    assert first.allowed
    item.block()
    assert service.check("C", CustomerContext()).code == "CUSTOMER_BLOCKED"
    item.activate()
    assert service.check("C", CustomerContext()).allowed
    assert first.allowed and item.status == "ACTIVE"
