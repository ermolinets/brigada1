import pytest
from decimal import Decimal
from datetime import date, datetime, timezone, timedelta
from app import api
from app.support.errors import DomainError


def assert_code(code, action):
    with pytest.raises(DomainError) as caught:
        action()
    assert caught.value.code == code

from app.support.types import money

from app.domain.customer import Customer

@pytest.mark.parametrize("state,action,target", [('ACTIVE', 'activate', None), ('ACTIVE', 'block', 'BLOCKED'), ('ACTIVE', 'close', 'CLOSED'), ('BLOCKED', 'activate', 'ACTIVE'), ('BLOCKED', 'block', None), ('BLOCKED', 'close', 'CLOSED'), ('CLOSED', 'activate', None), ('CLOSED', 'block', None), ('CLOSED', 'close', None)])
def test_review_transition_table_and_atomic_refusal(state, action, target):
    item = Customer("C1", "Alice", "STANDARD")
    paths = {'ACTIVE': (), 'BLOCKED': ('block',), 'CLOSED': ('close',)}
    for setup in paths[state]:
        getattr(item, setup)()
    before = api.view(item)
    if target is None:
        assert_code("INVALID_STATE", lambda: getattr(item, action)())
        assert api.view(item) == before
    else:
        getattr(item, action)()
        assert item.status == target
